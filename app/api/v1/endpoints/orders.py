import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Header, Request, status

from app.api.deps import DbSession, client_ip, require_editor
from app.core.config import settings
from app.core.exceptions import AppError, NotFoundError
from app.core.logging import get_logger
from app.models.order import OrderStatus
from app.rate_limit import limiter
from app.schemas.common import Page, PaginationParams
from app.schemas.order import OrderCreate, OrderRead, OrderSubmissionResponse, OrderUpdate
from app.services import email, order_service, service_service
from app.services.turnstile import verify_turnstile

logger = get_logger(__name__)

public_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(require_editor)])


class SpamRejectedError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "spam_rejected"


class UnpublishedServiceError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "service_unavailable"


@public_router.post(
    "",
    response_model=OrderSubmissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Place an order for a published service",
)
@limiter.limit(settings.rate_limit_orders)
async def submit_order(
    request: Request,
    db: DbSession,
    payload: OrderCreate,
    background: BackgroundTasks,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> OrderSubmissionResponse:
    if idempotency_key:
        existing = await order_service.get_by_idempotency_key(db, idempotency_key)
        if existing is not None:
            return OrderSubmissionResponse(id=existing.id)

    try:
        service = await service_service.get_by_id(db, payload.service_id)
    except NotFoundError as exc:
        raise UnpublishedServiceError("This service is not available to order") from exc
    if not service.is_published:
        raise UnpublishedServiceError("This service is not available to order")

    ip = client_ip(request)
    is_honeypot = bool(payload.website)
    if not is_honeypot and not await verify_turnstile(payload.turnstile_token, ip):
        raise SpamRejectedError("Bot verification failed. Please reload the page and try again.")

    order = await order_service.create_order(
        db,
        payload,
        service,
        ip_address=ip,
        user_agent=request.headers.get("user-agent"),
        idempotency_key=idempotency_key,
        status=OrderStatus.CANCELLED if is_honeypot else OrderStatus.NEW,
    )

    if not is_honeypot:
        logger.info("order_created", order_id=str(order.id), service=service.slug)
        background.add_task(email.notify_team_of_order, order)
        background.add_task(email.acknowledge_order, order)

    return OrderSubmissionResponse(id=order.id)


@admin_router.get("", response_model=Page[OrderRead])
async def list_orders(
    db: DbSession,
    pagination: Annotated[PaginationParams, Depends()],
    status_filter: OrderStatus | None = None,
    service_id: uuid.UUID | None = None,
    search: str | None = None,
) -> Page[OrderRead]:
    orders, total = await order_service.list_orders(
        db, pagination.offset, pagination.page_size, status_filter, service_id, search
    )
    return Page[OrderRead](
        items=[OrderRead.model_validate(order) for order in orders],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@admin_router.get("/stats", response_model=dict[str, int])
async def order_stats(db: DbSession) -> dict[str, int]:
    return await order_service.count_by_status(db)


@admin_router.get("/{order_id}", response_model=OrderRead)
async def read_order(db: DbSession, order_id: uuid.UUID) -> OrderRead:
    order = await order_service.get_by_id(db, order_id)
    return OrderRead.model_validate(order)


@admin_router.patch("/{order_id}", response_model=OrderRead)
async def update_order(db: DbSession, order_id: uuid.UUID, payload: OrderUpdate) -> OrderRead:
    order = await order_service.get_by_id(db, order_id)
    updated = await order_service.update_order(db, order, payload)
    return OrderRead.model_validate(updated)
