import asyncio

from app.core.config import get_settings
from app.db.session import AsyncSessionLocal
from app.repositories.in_memory import report_store, risk_store
from app.repositories.sql import SqlReportStore, SqlRiskStore
from app.services.ai_pipeline import ai_pipeline
from app.workers.celery_app import celery_app


async def process_report_async(report_reference: str) -> None:
    settings = get_settings()
    if settings.storage_backend == "postgres":
        async with AsyncSessionLocal() as session:
            await ai_pipeline.process_report(
                report_reference=report_reference,
                report_store=SqlReportStore(session),
                risk_store=SqlRiskStore(session),
            )
            await session.commit()
        return

    await ai_pipeline.process_report(
        report_reference=report_reference,
        report_store=report_store,
        risk_store=risk_store,
    )


@celery_app.task(name="app.workers.tasks.process_report")
def process_report(report_reference: str) -> None:
    asyncio.run(process_report_async(report_reference))
