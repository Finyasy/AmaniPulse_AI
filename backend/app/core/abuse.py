from collections import defaultdict, deque
from threading import Lock
from time import monotonic


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, key: str, limit: int, window_seconds: int) -> tuple[bool, int]:
        now = monotonic()
        window_start = now - window_seconds
        with self._lock:
            events = self._events[key]
            while events and events[0] < window_start:
                events.popleft()

            if len(events) >= limit:
                retry_after = max(1, int(window_seconds - (now - events[0])))
                return False, retry_after

            events.append(now)
            return True, 0

    def reset(self) -> None:
        with self._lock:
            self._events.clear()


report_rate_limiter = InMemoryRateLimiter()
