from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from app.domain.enums import IncidentCategory, LocationMode, ReportStatus, RiskLevel


class ConsentPayload(BaseModel):
    anonymous_submission: bool = Field(..., description="User consented to anonymous submission.")
    risk_analysis: bool = Field(
        ...,
        description="User consented to use in aggregated risk analysis.",
    )

    @model_validator(mode="after")
    def require_consents(self) -> "ConsentPayload":
        if not self.anonymous_submission or not self.risk_analysis:
            raise ValueError("anonymous_submission and risk_analysis consents are required")
        return self


class LocationPayload(BaseModel):
    mode: LocationMode
    country: str | None = Field(default=None, min_length=2, max_length=2)
    county: str | None = Field(default=None, max_length=80)
    area_label: str | None = Field(default=None, max_length=120)
    latitude_rounded: float | None = Field(default=None, ge=-90, le=90)
    longitude_rounded: float | None = Field(default=None, ge=-180, le=180)
    precision_km: int | None = Field(default=None, ge=1, le=50)

    @field_validator("country")
    @classmethod
    def uppercase_country(cls, value: str | None) -> str | None:
        return value.upper() if value is not None else None

    @model_validator(mode="after")
    def validate_location_mode(self) -> "LocationPayload":
        if self.mode == LocationMode.none:
            return self

        if self.mode == LocationMode.manual_area:
            if not self.country or not self.county:
                raise ValueError("manual_area location requires country and county")
            return self

        if self.mode == LocationMode.approximate_coordinates:
            required = [
                self.country,
                self.county,
                self.latitude_rounded,
                self.longitude_rounded,
                self.precision_km,
            ]
            if any(value is None for value in required):
                raise ValueError(
                    "approximate_coordinates location requires country, county, "
                    "rounded coordinates, and precision_km"
                )
            return self

        return self


class ReportCreate(BaseModel):
    client_report_id: str = Field(..., min_length=8, max_length=80)
    category: IncidentCategory
    description: str = Field(..., min_length=10, max_length=2000)
    incident_time: datetime
    location: LocationPayload
    language: Literal["en", "sw"] = "en"
    source: Literal["ios_citizen_app", "web_citizen_portal"] = "ios_citizen_app"
    app_version: str = Field(default="1.0.0", max_length=20)
    consents: ConsentPayload

    @model_validator(mode="after")
    def prevent_future_incident_time(self) -> "ReportCreate":
        now = datetime.now(UTC)
        incident_time = self.incident_time
        if incident_time.tzinfo is None:
            incident_time = incident_time.replace(tzinfo=UTC)
        if incident_time > now:
            raise ValueError("incident_time cannot be in the future")
        return self


class ReportReceipt(BaseModel):
    report_reference: str
    status: ReportStatus
    received_at: datetime
    message: str


class ReportStatusResponse(BaseModel):
    report_reference: str
    status: ReportStatus
    updated_at: datetime
    display_message: str


class ReviewReportSummary(BaseModel):
    report_reference: str
    category: IncidentCategory
    status: ReportStatus
    incident_time: datetime
    received_at: datetime
    updated_at: datetime
    county: str | None
    area_label: str | None
    language: str
    severity_score: int | None = None
    risk_score: int | None = None
    confidence: float | None = None
    urgency: str | None = None
    review_priority: str | None = None
    recommended_action: str | None = None
    needs_human_review: bool | None = None


class ReviewReportDetail(ReviewReportSummary):
    description: str
    ai_labels: dict[str, str | int | float | bool]


class ReviewQueueResponse(BaseModel):
    reports: list[ReviewReportSummary]


class ReviewDecisionRequest(BaseModel):
    status: Literal["aggregated", "closed", "unable_to_process"]
    reviewer_id: str | None = Field(default=None, min_length=2, max_length=80)
    note: str = Field(..., min_length=3, max_length=500)


class ReviewDecisionResponse(BaseModel):
    report_reference: str
    status: ReportStatus
    updated_at: datetime
    reviewer_id: str
    note: str


class ReviewEventItem(BaseModel):
    report_reference: str
    reviewer_id: str
    previous_status: ReportStatus
    new_status: ReportStatus
    note: str
    created_at: datetime


class ReviewEventsResponse(BaseModel):
    events: list[ReviewEventItem]


class IncidentTaxonomyItem(BaseModel):
    id: IncidentCategory
    name: str
    description: str
    safety_guidance: str


class IncidentTaxonomyResponse(BaseModel):
    language: Literal["en", "sw"]
    categories: list[IncidentTaxonomyItem]


class CountyRiskResponse(BaseModel):
    county_code: str
    county_name: str
    risk_level: RiskLevel
    score: int = Field(..., ge=0, le=100)
    updated_at: datetime
    summary: str
    guidance: list[str]


class AppConfigResponse(BaseModel):
    minimum_supported_version: str
    feature_flags: dict[str, bool]
    emergency_disclaimer: str
    support_channels: dict[str, str]


class ResourceItem(BaseModel):
    id: str
    title: str
    body: str
    category: str
    updated_at: datetime


class ResourcesResponse(BaseModel):
    language: Literal["en", "sw"]
    country: Literal["KE"]
    resources: list[ResourceItem]


class ErrorDetail(BaseModel):
    code: str
    message: str
    retryable: bool = False


class ErrorResponse(BaseModel):
    error: ErrorDetail
