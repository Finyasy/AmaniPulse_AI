from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

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
    source: Literal["ios_citizen_app"] = "ios_citizen_app"
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
