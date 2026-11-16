"""Sliding-window log rate limiter: at most `limit` events per `window` seconds."""
import threading
import time
from collections import deque
from typing import Callable, Deque


class SlidingWindowRateLimiter:
    """Allows at most ``limit`` events within any ``window``-second interval.

    Unlike a token bucket it never permits a burst larger than ``limit`` across
    a window boundary, at the cost of O(limit) memory for the event log.
    """

    def __init__(self, limit: int, window: float, clock: Callable[[], float] = time.monotonic):
        if limit <= 0:
            raise ValueError("Limit must be positive")
        if window <= 0:
            raise ValueError("Window must be positive")
        self.limit = limit
        self.window = window
        self._clock = clock
        self._events: Deque[float] = deque()
        self._lock = threading.Lock()

    def _evict(self, now: float) -> None:
        cutoff = now - self.window
        while self._events and self._events[0] <= cutoff:
            self._events.popleft()

    def allow(self) -> bool:
        """Record an event if the window has room. Returns True if allowed."""
        with self._lock:
            now = self._clock()
            self._evict(now)
            if len(self._events) < self.limit:
                self._events.append(now)
                return True
            return False

    def remaining(self) -> int:
        """Number of events still allowed in the current window."""
        with self._lock:
            self._evict(self._clock())
            return self.limit - len(self._events)

    def retry_after(self) -> float:
        """Seconds until the next event would be allowed (0.0 if allowed now)."""
        with self._lock:
            now = self._clock()
            self._evict(now)
            if len(self._events) < self.limit:
                return 0.0
            return self._events[0] + self.window - now
