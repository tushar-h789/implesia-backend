import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Header, Request, status

from app.api.deps import DbSession, client_ip, require_editor
from app.core.config import settings
from app.core.exceptions import AppError
from app.core.logging import get_logger
from app.models.lead import LeadStatus
from app.rate_limit import limiter
from app.schemas.common import Page, PaginationParams
from app.schemas.lead import LeadCreate, LeadRead, LeadSubmissionResponse, LeadUpdate
from app.services import email, lead_service
from app.services.turnstile import verify_turnstile

logger = get_logger(__name__)

public_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(require_editor)])


class SpamRejectedError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "spam_rejected"


@public_router.post(
    "",
    response_model=LeadSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a project brief from the public contact form",
)
@limiter.limit(settings.rate_limit_leads)
async def submit_lead(
    request: Request,
    db: DbSession,
    payload: LeadCreate,
    background: BackgroundTasks,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> LeadSubmissionResponse:
    if idempotency_key:
        existing = await lead_service.get_by_idempotency_key(db, idempotency_key)
        if existing is not None:
            return LeadSubmissionResponse(id=existing.id)

    ip = client_ip(request)

    # Honeypot: quietly accept the submission but park it as spam so bots get
    # a success response and stop retrying.
    is_honeypot = bool(payload.website)
    if not is_honeypot and not await verify_turnstile(payload.turnstile_token, ip):
        raise SpamRejectedError("Bot verification failed. Please reload the page and try again.")

    lead = await lead_service.create_lead(
        db,
        payload,
        ip_address=ip,
        user_agent=request.headers.get("user-agent"),
        idempotency_key=idempotency_key,
        status=LeadStatus.SPAM if is_honeypot else LeadStatus.NEW,
    )

    if not is_honeypot:
        logger.info("lead_created", lead_id=str(lead.id), email=lead.email)
        background.add_task(email.notify_team_of_lead, lead)
        background.add_task(email.acknowledge_lead, lead)

    return LeadSubmissionResponse(id=lead.id)


@admin_router.get("", response_model=Page[LeadRead])
async def list_leads(
    db: DbSession,
    pagination: Annotated[PaginationParams, Depends()],
    status_filter: LeadStatus | None = None,
    search: str | None = None,
) -> Page[LeadRead]:
    leads, total = await lead_service.list_leads(
        db, pagination.offset, pagination.page_size, status_filter, search
    )
    return Page[LeadRead](
        items=[LeadRead.model_validate(lead) for lead in leads],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@admin_router.get("/stats", response_model=dict[str, int])
async def lead_stats(db: DbSession) -> dict[str, int]:
    return await lead_service.count_by_status(db)


@admin_router.get("/{lead_id}", response_model=LeadRead)
async def read_lead(db: DbSession, lead_id: uuid.UUID) -> LeadRead:
    lead = await lead_service.get_by_id(db, lead_id)
    return LeadRead.model_validate(lead)


@admin_router.patch("/{lead_id}", response_model=LeadRead)
async def update_lead(db: DbSession, lead_id: uuid.UUID, payload: LeadUpdate) -> LeadRead:
    lead = await lead_service.get_by_id(db, lead_id)
    updated = await lead_service.update_lead(db, lead, payload)
    return LeadRead.model_validate(updated)
