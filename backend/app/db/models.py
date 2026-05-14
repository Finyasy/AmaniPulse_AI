from datetime import UTC, datetime

from geoalchemy2 import Geometry
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_reference: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    client_report_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    description_ciphertext: Mapped[str] = mapped_column(Text)
    incident_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    location_mode: Mapped[str] = mapped_column(String(40), index=True)
    country: Mapped[str | None] = mapped_column(String(2), nullable=True, index=True)
    county_code: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)
    county: Mapped[str | None] = mapped_column(String(80), nullable=True, index=True)
    area_label: Mapped[str | None] = mapped_column(String(120), nullable=True)
    latitude_rounded: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude_rounded: Mapped[float | None] = mapped_column(Float, nullable=True)
    precision_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    language: Mapped[str] = mapped_column(String(8), index=True)
    source: Mapped[str] = mapped_column(String(40), index=True)
    app_version: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(40), index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    ai_labels: Mapped[dict[str, str | int | float | bool]] = mapped_column(
        JSONB,
        default=dict,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )


class ReviewEventModel(Base):
    __tablename__ = "review_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_reference: Mapped[str] = mapped_column(String(32), index=True)
    reviewer_id: Mapped[str] = mapped_column(String(80), index=True)
    previous_status: Mapped[str] = mapped_column(String(40), index=True)
    new_status: Mapped[str] = mapped_column(String(40), index=True)
    note: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        index=True,
    )


class InternalApiKeyModel(Base):
    __tablename__ = "internal_api_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    reviewer_id: Mapped[str] = mapped_column(String(80), index=True)
    role: Mapped[str] = mapped_column(String(40), default="reviewer", index=True)
    label: Mapped[str | None] = mapped_column(String(120), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CountyRiskModel(Base):
    __tablename__ = "county_risk"

    county_code: Mapped[str] = mapped_column(String(16), primary_key=True)
    county_name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    risk_level: Mapped[str] = mapped_column(String(20), index=True)
    score: Mapped[int] = mapped_column(Integer)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    summary: Mapped[str] = mapped_column(Text)
    guidance: Mapped[list[str]] = mapped_column(JSONB, default=list)
    centroid: Mapped[object | None] = mapped_column(
        Geometry("POINT", srid=4326),
        nullable=True,
    )
