"""Unit tests for SlidingWindowRateLimiter."""
import pytest
from utils.sliding_window import SlidingWindowRateLimiter


class FakeClock:
    def __init__(self) -> None:
        self.now = 100.0

    def __call__(self) -> float:
        return self.now


def test_allows_up_to_limit_then_blocks():
    limiter = SlidingWindowRateLimiter(3, 10, clock=FakeClock())
    assert [limiter.allow() for _ in range(4)] == [True, True, True, False]


def test_events_expire_after_window():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(2, 10, clock=clock)
    assert limiter.allow() and limiter.allow()
    assert not limiter.allow()
    clock.now += 10  # event at t=100 is exactly `window` old -> expired
    assert limiter.allow()


def test_no_double_burst_across_window_boundary():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(2, 10, clock=clock)
    clock.now = 109
    assert limiter.allow() and limiter.allow()
    clock.now = 111  # a fixed-window limiter would reset here
    assert not limiter.allow()


def test_remaining_and_retry_after():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(2, 10, clock=clock)
    assert limiter.remaining() == 2
    assert limiter.retry_after() == 0.0
    limiter.allow()
    clock.now += 4
    limiter.allow()
    assert limiter.remaining() == 0
    assert limiter.retry_after() == pytest.approx(6.0)
    clock.now += 6
    assert limiter.remaining() == 1
    assert limiter.retry_after() == 0.0


def test_rejected_calls_are_not_recorded():
    clock = FakeClock()
    limiter = SlidingWindowRateLimiter(1, 10, clock=clock)
    assert limiter.allow()
    clock.now += 5
    assert not limiter.allow()
    clock.now += 5
    assert limiter.allow()


@pytest.mark.parametrize("limit, window", [(0, 1), (-1, 1), (1, 0), (1, -5)])
def test_invalid_arguments(limit, window):
    with pytest.raises(ValueError):
        SlidingWindowRateLimiter(limit, window)
