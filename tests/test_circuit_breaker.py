"""Unit tests for CircuitBreaker."""
import pytest
from utils.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError, CircuitState


def test_validation():
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=10.0)
    assert cb.state == CircuitState.CLOSED
    with pytest.raises(ValueError, match="failure_threshold"):
        CircuitBreaker(failure_threshold=0)
    with pytest.raises(ValueError, match="recovery_timeout"):
        CircuitBreaker(recovery_timeout=-1.0)
    with pytest.raises(ValueError, match="success_threshold"):
        CircuitBreaker(success_threshold=0)


def test_circuit_tripping_and_rejection():
    cb = CircuitBreaker(failure_threshold=2)

    def failing():
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError):
        cb.call(failing)
    assert cb.state == CircuitState.CLOSED
    with pytest.raises(RuntimeError):
        cb.call(failing)
    assert cb.state == CircuitState.OPEN
    with pytest.raises(CircuitBreakerOpenError):
        cb.call(lambda: "success")


def test_half_open_recovery_and_failure(monkeypatch):
    current_time = 100.0
    monkeypatch.setattr("time.monotonic", lambda: current_time)

    cb = CircuitBreaker(failure_threshold=1, recovery_timeout=10.0, success_threshold=2)
    with pytest.raises(ValueError):
        cb.call(int, "invalid")
    assert cb.state == CircuitState.OPEN

    # Advance time to half-open
    current_time += 15.0
    assert cb.state == CircuitState.HALF_OPEN
    assert cb.call(lambda: "ok1") == "ok1"
    assert cb.state == CircuitState.HALF_OPEN
    assert cb.call(lambda: "ok2") == "ok2"
    assert cb.state == CircuitState.CLOSED

    # Failure in half-open immediately reopens
    with pytest.raises(ValueError):
        cb.call(int, "invalid")
    assert cb.state == CircuitState.OPEN
    current_time += 15.0
    assert cb.state == CircuitState.HALF_OPEN
    with pytest.raises(ValueError):
        cb.call(int, "invalid")
    assert cb.state == CircuitState.OPEN


def test_decorator_and_reset():
    cb = CircuitBreaker(failure_threshold=2)

    @cb
    def add(a: int, b: int) -> int:
        """Add numbers."""
        return a + b

    assert add(2, 3) == 5
    assert add.__name__ == "add"
    cb._state = CircuitState.OPEN
    with pytest.raises(CircuitBreakerOpenError):
        add(1, 1)

    cb.reset()
    assert cb.state == CircuitState.CLOSED
    assert add(1, 1) == 2
