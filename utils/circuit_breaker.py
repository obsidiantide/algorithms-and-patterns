"""Circuit Breaker pattern for fault tolerance and cascading failure prevention."""
from enum import Enum
import functools
import time
from typing import Any, Callable, Tuple, Type, Union


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpenError(Exception):
    """Raised when an operation is attempted while the circuit breaker is OPEN."""


class CircuitBreaker:
    """Circuit breaker state machine to handle external service failures."""

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 30.0,
        expected_exception: Union[Tuple[Type[Exception], ...], Type[Exception]] = Exception,
        success_threshold: int = 1,
    ) -> None:
        if failure_threshold <= 0:
            raise ValueError("failure_threshold must be positive")
        if recovery_timeout < 0:
            raise ValueError("recovery_timeout must be non-negative")
        if success_threshold <= 0:
            raise ValueError("success_threshold must be positive")

        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.success_threshold = success_threshold
        self.reset()

    @property
    def state(self) -> CircuitState:
        """Current state of the breaker, evaluating timeout if OPEN."""
        if self._state == CircuitState.OPEN and time.monotonic() - self._last_state_change >= self.recovery_timeout:
            self._state = CircuitState.HALF_OPEN
            self._success_count = 0
        return self._state

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """Execute callable wrapped by the circuit breaker."""
        if self.state == CircuitState.OPEN:
            raise CircuitBreakerOpenError("Circuit is OPEN; calls are rejected")
        try:
            result = func(*args, **kwargs)
        except self.expected_exception as exc:
            self._on_failure()
            raise exc
        self._on_success()
        return result

    def __call__(self, func: Callable) -> Callable:
        """Decorator interface for protecting a function."""
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return self.call(func, *args, **kwargs)
        return wrapper

    def _on_success(self) -> None:
        if self._state == CircuitState.HALF_OPEN:
            self._success_count += 1
            if self._success_count >= self.success_threshold:
                self.reset()
        else:
            self._failure_count = 0

    def _on_failure(self) -> None:
        self._failure_count += 1
        self._last_state_change = time.monotonic()
        if self._state == CircuitState.HALF_OPEN or self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN

    def reset(self) -> None:
        """Reset the circuit breaker back to initial CLOSED state."""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_state_change = time.monotonic()
