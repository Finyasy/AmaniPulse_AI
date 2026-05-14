import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SafetyAssessment:
    flags: tuple[str, ...]

    @property
    def pii_detected(self) -> bool:
        return len(self.flags) > 0

    @property
    def flag_count(self) -> int:
        return len(self.flags)

    @property
    def flag_summary(self) -> str:
        return ",".join(self.flags)


class SafetyService:
    _email_pattern = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
    _phone_pattern = re.compile(r"(?<!\d)(?:\+?254|0)\d{9}(?!\d)")
    _possible_id_pattern = re.compile(r"\b\d{7,9}\b")
    _address_hint_pattern = re.compile(
        r"\b(?:house|plot|flat|apartment|apt|room)\s+(?:no\.?\s*)?[A-Z0-9-]{1,12}\b",
        re.IGNORECASE,
    )

    def assess_text(self, text: str) -> SafetyAssessment:
        flags: list[str] = []
        if self._email_pattern.search(text):
            flags.append("email")
        if self._phone_pattern.search(text):
            flags.append("phone_number")
        if self._possible_id_pattern.search(text):
            flags.append("possible_id_number")
        if self._address_hint_pattern.search(text):
            flags.append("address_hint")
        return SafetyAssessment(flags=tuple(flags))


safety_service = SafetyService()
