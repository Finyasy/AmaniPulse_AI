from dataclasses import dataclass


@dataclass(frozen=True)
class InternalReviewerIdentity:
    reviewer_id: str
    role: str
    label: str | None = None
