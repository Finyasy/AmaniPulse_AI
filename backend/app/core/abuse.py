import re
from collections import defaultdict, deque
from hashlib import sha256
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


class DuplicateReportGuard:
    def __init__(self) -> None:
        self._fingerprints: dict[str, float] = {}
        self._lock = Lock()

    def assess(
        self,
        category: str,
        county: str | None,
        description: str,
        window_seconds: int,
    ) -> tuple[bool, str]:
        fingerprint = self._fingerprint(category, county, description)
        now = monotonic()
        with self._lock:
            expired_before = now - window_seconds
            expired = [
                key for key, timestamp in self._fingerprints.items() if timestamp < expired_before
            ]
            for key in expired:
                del self._fingerprints[key]

            duplicate = fingerprint in self._fingerprints
            self._fingerprints[fingerprint] = now
            return duplicate, fingerprint

    def reset(self) -> None:
        with self._lock:
            self._fingerprints.clear()

    def _fingerprint(self, category: str, county: str | None, description: str) -> str:
        normalized_text = re.sub(r"\s+", " ", description.strip().lower())
        normalized_county = (county or "unknown").strip().lower()
        payload = f"{category}|{normalized_county}|{normalized_text}"
        return sha256(payload.encode("utf-8")).hexdigest()


duplicate_report_guard = DuplicateReportGuard()
