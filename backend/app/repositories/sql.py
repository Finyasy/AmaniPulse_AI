from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.crypto import ReportCrypto
from app.db.models import CountyRiskModel, ReportModel, ReviewEventModel
from app.domain.enums import IncidentCategory, LocationMode, ReportStatus, RiskLevel
from app.domain.records import ReportRecord
from app.domain.review import ReviewEventRecord
from app.domain.schemas import CountyRiskResponse, LocationPayload


class SqlReportStore:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._crypto = ReportCrypto(get_settings().report_encryption_key)

    async def create(self, record: ReportRecord) -> ReportRecord:
        existing = await self._session.scalar(
            select(ReportModel).where(ReportModel.client_report_id == record.client_report_id)
        )
        if existing is not None:
            return self._to_record(existing)

        model = ReportModel(
            report_reference=record.report_reference,
            client_report_id=record.client_report_id,
            category=record.category.value,
            description_ciphertext=self._crypto.encrypt_text(record.description),
            incident_time=record.incident_time,
            location_mode=record.location.mode.value,
            country=record.location.country,
            county_code=record.location.county_code,
            county=record.location.county,
            area_label=record.location.area_label,
            latitude_rounded=record.location.latitude_rounded,
            longitude_rounded=record.location.longitude_rounded,
            precision_km=record.location.precision_km,
            language=record.language,
            source=record.source,
            app_version=record.app_version,
            status=record.status.value,
            received_at=record.received_at,
            updated_at=record.updated_at,
            ai_labels=record.ai_labels,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_record(model)

    async def get(self, report_reference: str) -> ReportRecord | None:
        model = await self._session.scalar(
            select(ReportModel).where(ReportModel.report_reference == report_reference)
        )
        if model is None:
            return None
        return self._to_record(model)

    async def update_status(
        self,
        report_reference: str,
        status: ReportStatus,
        ai_labels: dict[str, str | int | float | bool] | None = None,
    ) -> ReportRecord | None:
        model = await self._session.scalar(
            select(ReportModel).where(ReportModel.report_reference == report_reference)
        )
        if model is None:
            return None

        model.status = status.value
        model.updated_at = datetime.now(UTC)
        if ai_labels:
            model.ai_labels = {**model.ai_labels, **ai_labels}

        await self._session.flush()
        await self._session.refresh(model)
        return self._to_record(model)

    async def list_by_status(
        self,
        status: ReportStatus,
        limit: int = 50,
    ) -> list[ReportRecord]:
        result = await self._session.scalars(
            select(ReportModel)
            .where(ReportModel.status == status.value)
            .order_by(ReportModel.updated_at.desc())
            .limit(limit)
        )
        return [self._to_record(model) for model in result.all()]

    async def add_review_event(self, event: ReviewEventRecord) -> ReviewEventRecord:
        model = ReviewEventModel(
            report_reference=event.report_reference,
            reviewer_id=event.reviewer_id,
            previous_status=event.previous_status.value,
            new_status=event.new_status.value,
            note=event.note,
            created_at=event.created_at,
        )
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_review_event(model)

    async def list_review_events(
        self,
        report_reference: str,
        limit: int = 50,
    ) -> list[ReviewEventRecord]:
        result = await self._session.scalars(
            select(ReviewEventModel)
            .where(ReviewEventModel.report_reference == report_reference)
            .order_by(ReviewEventModel.created_at.desc())
            .limit(limit)
        )
        return [self._to_review_event(model) for model in result.all()]

    def _to_record(self, model: ReportModel) -> ReportRecord:
        return ReportRecord(
            report_reference=model.report_reference,
            client_report_id=model.client_report_id,
            category=IncidentCategory(model.category),
            description=self._crypto.decrypt_text(model.description_ciphertext),
            incident_time=model.incident_time,
            location=LocationPayload(
                mode=LocationMode(model.location_mode),
                country=model.country,
                county_code=model.county_code,
                county=model.county,
                area_label=model.area_label,
                latitude_rounded=model.latitude_rounded,
                longitude_rounded=model.longitude_rounded,
                precision_km=model.precision_km,
            ),
            language=model.language,
            source=model.source,
            app_version=model.app_version,
            status=ReportStatus(model.status),
            received_at=model.received_at,
            updated_at=model.updated_at,
            ai_labels=model.ai_labels or {},
        )

    def _to_review_event(self, model: ReviewEventModel) -> ReviewEventRecord:
        return ReviewEventRecord(
            report_reference=model.report_reference,
            reviewer_id=model.reviewer_id,
            previous_status=ReportStatus(model.previous_status),
            new_status=ReportStatus(model.new_status),
            note=model.note,
            created_at=model.created_at,
        )


class SqlRiskStore:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, county_code: str) -> CountyRiskResponse | None:
        model = await self._session.get(CountyRiskModel, county_code.upper())
        if model is None:
            return None
        return self._to_response(model)

    async def county_code_for_name(self, county_name: str | None) -> str | None:
        if county_name is None:
            return None
        model = await self._session.scalar(
            select(CountyRiskModel).where(CountyRiskModel.county_name.ilike(county_name))
        )
        return model.county_code if model is not None else None

    async def county_name_for_code(self, county_code: str | None) -> str | None:
        if county_code is None:
            return None
        model = await self._session.get(CountyRiskModel, county_code.upper())
        return model.county_name if model is not None else None

    async def bump_for_report(
        self,
        county_name: str | None,
        severity_score: int,
        county_code: str | None = None,
    ) -> CountyRiskResponse | None:
        resolved_county_code = county_code or await self.county_code_for_name(county_name)
        if resolved_county_code is None:
            return None

        model = await self._session.get(CountyRiskModel, resolved_county_code.upper())
        if model is None:
            return None

        score = min(100, model.score + max(1, severity_score // 10))
        model.score = score
        model.risk_level = self._level_for_score(score).value
        model.updated_at = datetime.now(UTC)
        model.summary = (
            "Recent anonymous reporting has been included in aggregated county guidance."
        )

        await self._session.flush()
        await self._session.refresh(model)
        return self._to_response(model)

    def _level_for_score(self, score: int) -> RiskLevel:
        if score >= 80:
            return RiskLevel.critical
        if score >= 65:
            return RiskLevel.high
        if score >= 40:
            return RiskLevel.moderate
        return RiskLevel.low

    def _to_response(self, model: CountyRiskModel) -> CountyRiskResponse:
        return CountyRiskResponse(
            county_code=model.county_code,
            county_name=model.county_name,
            risk_level=RiskLevel(model.risk_level),
            score=model.score,
            updated_at=model.updated_at,
            summary=model.summary,
            guidance=model.guidance or [],
        )
