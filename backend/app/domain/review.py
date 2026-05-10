from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import ReportStatus


@dataclass(slots=True)
class ReviewEventRecord:
    report_reference: str
    reviewer_id: str
    previous_status: ReportStatus
    new_status: ReportStatus
    note: str
    created_at: datetime
