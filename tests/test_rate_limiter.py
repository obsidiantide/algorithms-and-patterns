"""Unit tests for TokenBucketRateLimiter."""
import pytest
from utils.rate_limiter import TokenBucketRateLimiter


def test_initial_capacity():
    limiter = TokenBucketRateLimiter(capacity=10, refill_rate=1.0)
    assert limiter.capacity == 10.0
    assert limiter.tokens == 10.0


def test_consume_single_token():
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1.0)
    assert limiter.consume() is True
    assert limiter.tokens == 4.0


def test_consume_multiple_tokens():
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1.0)
    assert limiter.consume(3) is True
    assert limiter.tokens == 2.0


def test_consume_exhaustion():
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate=1.0)
    assert limiter.consume(2) is True
    assert limiter.consume(1) is False


def test_consume_more_than_capacity():
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1.0)
    assert limiter.consume(6) is False


def test_refill_replenishes_tokens(monkeypatch):
    current_time = 1000.0
    monkeypatch.setattr("time.monotonic", lambda: current_time)

    limiter = TokenBucketRateLimiter(capacity=10, refill_rate=2.0)
    assert limiter.consume(10) is True
    assert limiter.consume(1) is False

    # 1.5 seconds pass -> 3 tokens replenished
    current_time += 1.5
    assert limiter.consume(3) is True
    assert limiter.consume(1) is False


def test_refill_capped_at_capacity(monkeypatch):
    current_time = 1000.0
    monkeypatch.setattr("time.monotonic", lambda: current_time)

    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=2.0)
    assert limiter.consume(3) is True

    # Long time passes -> tokens should cap at capacity (5)
    current_time += 100.0
    assert limiter.consume(1) is True
    assert limiter.tokens == 4.0
    assert limiter.consume(4) is True
    assert limiter.consume(1) is False


def test_invalid_capacity_or_refill_rate():
    with pytest.raises(ValueError, match="Capacity must be positive"):
        TokenBucketRateLimiter(capacity=0, refill_rate=1.0)
    with pytest.raises(ValueError, match="Capacity must be positive"):
        TokenBucketRateLimiter(capacity=-5, refill_rate=1.0)
    with pytest.raises(ValueError, match="Refill rate must be non-negative"):
        TokenBucketRateLimiter(capacity=5, refill_rate=-1.0)


def test_invalid_tokens_to_consume():
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate=1.0)
    with pytest.raises(ValueError, match="Tokens to consume must be positive"):
        limiter.consume(0)
    with pytest.raises(ValueError, match="Tokens to consume must be positive"):
        limiter.consume(-2)


def test_concurrent_consume_never_exceeds_capacity():
    import threading

    limiter = TokenBucketRateLimiter(capacity=100, refill_rate=0.0)
    granted = []
    barrier = threading.Barrier(8)

    def worker():
        barrier.wait()
        count = 0
        for _ in range(100):
            if limiter.consume():
                count += 1
        granted.append(count)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert sum(granted) == 100
    assert limiter.tokens == 0.0
