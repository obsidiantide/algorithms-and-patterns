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


def _run_threads(target, count=8):
    import threading

    barrier = threading.Barrier(count)

    def runner():
        barrier.wait()
        target()

    threads = [threading.Thread(target=runner) for _ in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def test_concurrent_failures_are_all_counted_and_trip_the_breaker():
    import threading
    import time

    breaker = CircuitBreaker(failure_threshold=10_000, recovery_timeout=60)
    executed = []
    lock = threading.Lock()

    def failing():
        with lock:
            executed.append(1)
        time.sleep(0)
        raise ValueError("boom")

    def worker():
        for _ in range(200):
            try:
                breaker.call(failing)
            except ValueError:
                pass

    _run_threads(worker)

    assert len(executed) == 1600
    assert breaker._failure_count == 1600
    assert breaker.state == CircuitState.CLOSED


def test_concurrent_calls_reject_once_open_and_never_lose_state():
    import threading

    breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
    outcomes = {"failed": 0, "rejected": 0}
    lock = threading.Lock()

    def failing():
        raise RuntimeError("down")

    def worker():
        for _ in range(100):
            try:
                breaker.call(failing)
            except CircuitBreakerOpenError:
                with lock:
                    outcomes["rejected"] += 1
            except RuntimeError:
                with lock:
                    outcomes["failed"] += 1

    _run_threads(worker)

    assert outcomes["failed"] + outcomes["rejected"] == 800
    assert outcomes["failed"] >= 5
    assert outcomes["rejected"] > 0
    assert breaker.state == CircuitState.OPEN


def test_concurrent_half_open_successes_close_the_circuit(monkeypatch):
    import utils.circuit_breaker as module

    now = [1000.0]
    monkeypatch.setattr(module.time, "monotonic", lambda: now[0])
    breaker = CircuitBreaker(failure_threshold=1, recovery_timeout=10, success_threshold=4)

    with pytest.raises(ValueError):
        breaker.call(lambda: (_ for _ in ()).throw(ValueError("x")))
    assert breaker.state == CircuitState.OPEN

    now[0] += 10
    assert breaker.state == CircuitState.HALF_OPEN

    _run_threads(lambda: breaker.call(lambda: "ok"))

    assert breaker.state == CircuitState.CLOSED
    assert breaker._failure_count == 0
