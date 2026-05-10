import asyncio
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest
import sqlalchemy as sa
from alembic.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from alembic import command
from app.core.config import get_settings
from app.domain.enums import IncidentCategory, LocationMode, ReportStatus
from app.domain.records import ReportRecord
from app.domain.schemas import LocationPayload
from app.repositories.sql import SqlReportStore, SqlRiskStore
from app.services.ai_pipeline import ai_pipeline
from app.services.review_service import review_service

if os.getenv("RUN_POSTGRES_TESTS") != "1":
    pytest.skip(
        "Set RUN_POSTGRES_TESTS=1 to run Docker/Postgres integration tests.",
        allow_module_level=True,
    )


def test_postgres_migrations_and_county_seed() -> None:
    _upgrade_database()

    async def check_seed() -> None:
        engine = _engine()
        async with engine.connect() as connection:
            county_count = await connection.scalar(sa.text("SELECT count(*) FROM county_risk"))
            revision = await connection.scalar(sa.text("SELECT version_num FROM alembic_version"))
            nairobi = await connection.execute(
                sa.text(
                    """
                    SELECT county_name, risk_level, score
                    FROM county_risk
                    WHERE county_code = 'KE-047'
                    """
                )
            )
            row = nairobi.one()

        await engine.dispose()
        assert county_count == 47
        assert revision == "20260510_0004"
        assert row.county_name == "Nairobi"
        assert row.risk_level in {"low", "moderate", "high", "critical"}
        assert 0 <= row.score <= 100

    asyncio.run(check_seed())


def test_postgres_encryption_processing_and_review_audit() -> None:
    _upgrade_database()

    async def exercise_flow() -> None:
        engine = _engine()
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        async with session_factory() as session:
            report_store = SqlReportStore(session)
            risk_store = SqlRiskStore(session)
            plaintext = f"Sensitive report probe {uuid4()} about attack warnings."
            report = ReportRecord(
                report_reference=f"AP-IT-{uuid4().hex[:8].upper()}",
                client_report_id=f"integration-{uuid4()}",
                category=IncidentCategory.violence_threat,
                description=plaintext,
                incident_time=datetime.now(UTC) - timedelta(minutes=5),
                location=LocationPayload(
                    mode=LocationMode.manual_area,
                    country="KE",
                    county="Nairobi",
                    area_label="Kasarani",
                ),
                language="en",
                source="ios_citizen_app",
                app_version="1.0.0",
                status=ReportStatus.received,
                received_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )

            created = await report_store.create(report)
            raw_ciphertext = await session.scalar(
                sa.text(
                    """
                    SELECT description_ciphertext
                    FROM reports
                    WHERE report_reference = :report_reference
                    """
                ),
                {"report_reference": created.report_reference},
            )
            assert raw_ciphertext is not None
            assert plaintext not in raw_ciphertext
            assert raw_ciphertext.startswith("gAAAAA")

            retrieved = await report_store.get(created.report_reference)
            assert retrieved is not None
            assert retrieved.description == plaintext

            await ai_pipeline.process_report(
                report_reference=created.report_reference,
                report_store=report_store,
                risk_store=risk_store,
            )
            processed = await report_store.get(created.report_reference)
            assert processed is not None
            assert processed.status == ReportStatus.under_review

            decision = await review_service.apply_decision(
                report_reference=created.report_reference,
                status=ReportStatus.aggregated,
                reviewer_id="integration-reviewer",
                note="Validated by integration test.",
                store=report_store,
            )
            assert decision is not None
            events = await review_service.list_review_events(
                report_reference=created.report_reference,
                store=report_store,
                limit=10,
            )
            assert events is not None
            assert events[0].previous_status == ReportStatus.under_review
            assert events[0].new_status == ReportStatus.aggregated
            await session.commit()

        await engine.dispose()

    asyncio.run(exercise_flow())


def _upgrade_database() -> None:
    alembic_config = Config(str(Path(__file__).parents[2] / "alembic.ini"))
    command.upgrade(alembic_config, "head")


def _engine():
    return create_async_engine(
        get_settings().database_url,
        pool_pre_ping=True,
        poolclass=NullPool,
    )
