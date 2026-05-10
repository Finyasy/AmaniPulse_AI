from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enums import IncidentCategory, LocationMode, ReportStatus
from app.domain.schemas import LocationPayload


@dataclass(slots=True)
class ReportRecord:
    report_reference: str
    client_report_id: str
    category: IncidentCategory
    description: str
    incident_time: datetime
    location: LocationPayload
    language: str
    source: str
    app_version: str
    status: ReportStatus
    received_at: datetime
    updated_at: datetime
    ai_labels: dict[str, str | int | float | bool] = field(default_factory=dict)

    @property
    def county(self) -> str | None:
        if self.location.mode == LocationMode.none:
            return None
        return self.location.county
