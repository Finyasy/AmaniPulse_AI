from collections.abc import AsyncIterator

from app.core.config import get_settings
from app.db.session import get_db_session
from app.repositories.in_memory import report_store, risk_store
from app.repositories.protocols import ReportStore, RiskStore
from app.repositories.sql import SqlReportStore, SqlRiskStore


async def get_report_store(
) -> AsyncIterator[ReportStore]:
    if get_settings().storage_backend != "postgres":
        yield report_store
        return

    async for session in get_db_session():
        yield SqlReportStore(session)


async def get_risk_store(
) -> AsyncIterator[RiskStore]:
    if get_settings().storage_backend != "postgres":
        yield risk_store
        return

    async for session in get_db_session():
        yield SqlRiskStore(session)
