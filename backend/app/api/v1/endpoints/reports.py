from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_report_store
from app.core.config import get_settings
from app.domain.schemas import ReportCreate, ReportReceipt, ReportStatusResponse
from app.repositories.protocols import ReportStore
from app.services.report_service import report_service
from app.workers.tasks import process_report, process_report_async

router = APIRouter()
ReportStoreDep = Annotated[ReportStore, Depends(get_report_store)]


@router.post("/reports", response_model=ReportReceipt, status_code=status.HTTP_201_CREATED)
async def submit_report(
    payload: ReportCreate,
    store: ReportStoreDep,
) -> ReportReceipt:
    receipt, record = await report_service.submit_report(payload, store=store)
    if get_settings().celery_task_always_eager:
        await process_report_async(record.report_reference)
    else:
        process_report.delay(record.report_reference)
    return receipt


@router.get("/reports/{report_reference}/status", response_model=ReportStatusResponse)
async def get_report_status(
    report_reference: str,
    store: ReportStoreDep,
) -> ReportStatusResponse:
    status_response = await report_service.get_report_status(report_reference, store=store)
    if status_response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "report_not_found",
                "message": "No report was found for that reference.",
            },
        )
    return status_response
