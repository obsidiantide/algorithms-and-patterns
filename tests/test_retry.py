"""Unit tests for retry_with_backoff utility decorator."""
import pytest
from utils.retry import retry_with_backoff


def test_retry_success_first_attempt(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr("time.sleep", sleep_calls.append)

    call_count = 0

    @retry_with_backoff(retries=3, initial_delay=0.1)
    def compute(x: int) -> int:
        nonlocal call_count
        call_count += 1
        return x * 2

    assert compute(5) == 10
    assert call_count == 1
    assert sleep_calls == []


def test_retry_success_after_transient_failures(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr("time.sleep", sleep_calls.append)

    call_count = 0

    @retry_with_backoff(retries=3, initial_delay=0.1, exceptions=(ValueError,))
    def flaky_service():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError(f"Temporary failure {call_count}")
        return "success"

    assert flaky_service() == "success"
    assert call_count == 3
    assert len(sleep_calls) == 2


def test_retry_exhaustion_raises_last_error(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr("time.sleep", sleep_calls.append)

    call_count = 0

    @retry_with_backoff(retries=3, initial_delay=0.1, exceptions=(RuntimeError,))
    def always_fails():
        nonlocal call_count
        call_count += 1
        raise RuntimeError(f"Failure {call_count}")

    with pytest.raises(RuntimeError, match="Failure 3"):
        always_fails()

    assert call_count == 3
    assert len(sleep_calls) == 2


def test_unhandled_exception_raises_immediately(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr("time.sleep", sleep_calls.append)

    call_count = 0

    @retry_with_backoff(retries=3, initial_delay=0.1, exceptions=(ValueError,))
    def raises_unhandled():
        nonlocal call_count
        call_count += 1
        raise TypeError("Unexpected type error")

    with pytest.raises(TypeError, match="Unexpected type error"):
        raises_unhandled()

    assert call_count == 1
    assert sleep_calls == []


def test_single_exception_type_argument(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr("time.sleep", sleep_calls.append)

    call_count = 0

    @retry_with_backoff(retries=2, initial_delay=0.01, exceptions=ValueError)
    def operation():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ValueError("First attempt failed")
        return "ok"

    assert operation() == "ok"
    assert call_count == 2
    assert len(sleep_calls) == 1


def test_exponential_backoff_progression(monkeypatch):
    sleep_calls = []
    monkeypatch.setattr("time.sleep", sleep_calls.append)
    monkeypatch.setattr("random.uniform", lambda a, b: 0.0)

    @retry_with_backoff(retries=4, initial_delay=1.0, backoff_factor=2.0)
    def failing():
        raise Exception("error")

    with pytest.raises(Exception):
        failing()

    assert sleep_calls == [1.0, 2.0, 4.0]


def test_preserves_function_metadata():
    @retry_with_backoff(retries=2)
    def documented_func(a: int) -> int:
        """Calculate something important."""
        return a + 1

    assert documented_func.__name__ == "documented_func"
    assert documented_func.__doc__ == "Calculate something important."


def test_invalid_parameters():
    with pytest.raises(ValueError, match="retries must be at least 1"):
        retry_with_backoff(retries=0)

    with pytest.raises(ValueError, match="initial_delay must be non-negative"):
        retry_with_backoff(initial_delay=-0.5)

    with pytest.raises(ValueError, match="backoff_factor must be at least 1.0"):
        retry_with_backoff(backoff_factor=0.5)

    with pytest.raises(TypeError, match="exceptions must be an Exception subclass"):
        retry_with_backoff(exceptions="not_an_exception")  # type: ignore
