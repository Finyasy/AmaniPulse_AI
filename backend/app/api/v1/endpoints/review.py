from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status

from app.api.deps import get_report_store
from app.core.config import get_settings
from app.domain.enums import ReportStatus
from app.domain.schemas import (
    ReviewDecisionRequest,
    ReviewDecisionResponse,
    ReviewEventsResponse,
    ReviewQueueResponse,
    ReviewReportDetail,
)
from app.repositories.protocols import ReportStore
from app.services.review_service import review_service

router = APIRouter(prefix="/internal/review")
ReportStoreDep = Annotated[ReportStore, Depends(get_report_store)]


async def require_internal_token(
    x_internal_token: Annotated[str | None, Header()] = None,
) -> None:
    if x_internal_token != get_settings().internal_api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "unauthorized",
                "message": "A valid internal token is required.",
            },
        )


InternalAuthDep = Annotated[None, Depends(require_internal_token)]


@router.get("/queue", response_model=ReviewQueueResponse)
async def list_review_queue(
    _auth: InternalAuthDep,
    store: ReportStoreDep,
    limit: int = Query(default=50, ge=1, le=100),
) -> ReviewQueueResponse:
    reports = await review_service.list_review_queue(store=store, limit=limit)
    return ReviewQueueResponse(reports=reports)


@router.get("/reports/{report_reference}", response_model=ReviewReportDetail)
async def get_review_report(
    report_reference: str,
    _auth: InternalAuthDep,
    store: ReportStoreDep,
) -> ReviewReportDetail:
    report = await review_service.get_review_report(report_reference, store=store)
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "report_not_found",
                "message": "No report was found for that reference.",
            },
        )
    return report


@router.post("/reports/{report_reference}/decision", response_model=ReviewDecisionResponse)
async def apply_review_decision(
    report_reference: str,
    payload: ReviewDecisionRequest,
    _auth: InternalAuthDep,
    store: ReportStoreDep,
) -> ReviewDecisionResponse:
    decision = await review_service.apply_decision(
        report_reference=report_reference,
        status=ReportStatus(payload.status),
        reviewer_id=payload.reviewer_id,
        note=payload.note,
        store=store,
    )
    if decision is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "report_not_found",
                "message": "No report was found for that reference.",
            },
        )
    return decision


@router.get("/reports/{report_reference}/events", response_model=ReviewEventsResponse)
async def list_review_events(
    report_reference: str,
    _auth: InternalAuthDep,
    store: ReportStoreDep,
    limit: int = Query(default=50, ge=1, le=100),
) -> ReviewEventsResponse:
    events = await review_service.list_review_events(
        report_reference=report_reference,
        store=store,
        limit=limit,
    )
    if events is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "report_not_found",
                "message": "No report was found for that reference.",
            },
        )
    return ReviewEventsResponse(events=events)
