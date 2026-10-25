"""Decorator for retrying operations with exponential backoff and jitter."""
import functools
import logging
import random
import time
from typing import Any, Callable, Tuple, Type, Union

logger = logging.getLogger(__name__)


def retry_with_backoff(
    retries: int = 3,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
    exceptions: Union[Tuple[Type[Exception], ...], Type[Exception]] = (Exception,),
) -> Callable:
    """Retry a function with exponential backoff upon specified exceptions."""
    if retries < 1:
        raise ValueError("retries must be at least 1")
    if initial_delay < 0:
        raise ValueError("initial_delay must be non-negative")
    if backoff_factor < 1.0:
        raise ValueError("backoff_factor must be at least 1.0")

    if isinstance(exceptions, type) and issubclass(exceptions, Exception):
        exc_types: Tuple[Type[Exception], ...] = (exceptions,)
    elif isinstance(exceptions, tuple) and all(
        isinstance(e, type) and issubclass(e, Exception) for e in exceptions
    ):
        exc_types = exceptions
    else:
        raise TypeError("exceptions must be an Exception subclass or tuple of Exception subclasses")

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_err = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exc_types as e:
                    last_err = e
                    if attempt == retries:
                        break
                    sleep_time = delay + random.uniform(0, 0.1 * delay)
                    logger.warning(
                        f"Attempt {attempt}/{retries} failed for {func.__name__}: {e}. Retrying in {sleep_time:.2f}s"
                    )
                    time.sleep(sleep_time)
                    delay *= backoff_factor
            raise last_err

        return wrapper

    return decorator
