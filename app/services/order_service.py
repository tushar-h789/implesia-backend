import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError
from app.models.order import Order, OrderStatus
from app.models.service import Service
from app.schemas.order import OrderCreate, OrderUpdate


async def get_by_id(db: AsyncSession, order_id: uuid.UUID) -> Order:
    result = await db.execute(
        select(Order).options(selectinload(Order.service)).where(Order.id == order_id)
    )
    order = result.scalar_one_or_none()
    if order is None:
        raise NotFoundError("Order not found")
    return order


async def get_by_idempotency_key(db: AsyncSession, key: str) -> Order | None:
    result = await db.execute(
        select(Order).options(selectinload(Order.service)).where(Order.idempotency_key == key)
    )
    return result.scalar_one_or_none()


async def list_orders(
    db: AsyncSession,
    offset: int,
    limit: int,
    status: OrderStatus | None = None,
    service_id: uuid.UUID | None = None,
    search: str | None = None,
) -> tuple[list[Order], int]:
    filters = []
    if status is not None:
        filters.append(Order.status == status)
    if service_id is not None:
        filters.append(Order.service_id == service_id)
    if search:
        pattern = f"%{search.lower()}%"
        filters.append(
            func.lower(Order.full_name).like(pattern)
            | func.lower(Order.email).like(pattern)
            | func.lower(Order.organisation).like(pattern)
        )

    total = await db.scalar(select(func.count()).select_from(Order).where(*filters)) or 0
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.service))
        .where(*filters)
        .order_by(Order.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return list(result.scalars().all()), total


async def create_order(
    db: AsyncSession,
    payload: OrderCreate,
    service: Service,
    *,
    ip_address: str | None,
    user_agent: str | None,
    idempotency_key: str | None,
    status: OrderStatus = OrderStatus.NEW,
) -> Order:
    order = Order(
        service_id=service.id,
        full_name=payload.full_name,
        email=payload.email.lower(),
        phone=payload.phone,
        organisation=payload.organisation,
        message=payload.message,
        status=status,
        source_page=payload.source_page,
        ip_address=ip_address,
        user_agent=user_agent[:512] if user_agent else None,
        idempotency_key=idempotency_key,
    )
    db.add(order)
    await db.commit()
    return await get_by_id(db, order.id)


async def update_order(db: AsyncSession, order: Order, payload: OrderUpdate) -> Order:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    await db.commit()
    return await get_by_id(db, order.id)


async def count_by_status(db: AsyncSession) -> dict[str, int]:
    result = await db.execute(select(Order.status, func.count()).group_by(Order.status))
    counts = {status.value: 0 for status in OrderStatus}
    for status, count in result.all():
        counts[status.value] = count
    return counts
