import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.lead import Lead, LeadStatus
from app.schemas.lead import LeadCreate, LeadUpdate


async def get_by_id(db: AsyncSession, lead_id: uuid.UUID) -> Lead:
    lead = await db.get(Lead, lead_id)
    if lead is None:
        raise NotFoundError("Lead not found")
    return lead


async def get_by_idempotency_key(db: AsyncSession, key: str) -> Lead | None:
    result = await db.execute(select(Lead).where(Lead.idempotency_key == key))
    return result.scalar_one_or_none()


async def list_leads(
    db: AsyncSession,
    offset: int,
    limit: int,
    status: LeadStatus | None = None,
    search: str | None = None,
) -> tuple[list[Lead], int]:
    filters = []
    if status is not None:
        filters.append(Lead.status == status)
    if search:
        pattern = f"%{search.lower()}%"
        filters.append(
            func.lower(Lead.full_name).like(pattern)
            | func.lower(Lead.email).like(pattern)
            | func.lower(Lead.organisation).like(pattern)
        )

    total = await db.scalar(select(func.count()).select_from(Lead).where(*filters)) or 0
    result = await db.execute(
        select(Lead).where(*filters).order_by(Lead.created_at.desc()).offset(offset).limit(limit)
    )
    return list(result.scalars().all()), total


async def create_lead(
    db: AsyncSession,
    payload: LeadCreate,
    *,
    ip_address: str | None,
    user_agent: str | None,
    idempotency_key: str | None,
    status: LeadStatus = LeadStatus.NEW,
) -> Lead:
    lead = Lead(
        full_name=payload.full_name,
        email=payload.email.lower(),
        phone=payload.phone,
        organisation=payload.organisation,
        service_area=payload.service_area,
        timeline=payload.timeline,
        brief=payload.brief,
        status=status,
        source_page=payload.source_page,
        ip_address=ip_address,
        user_agent=user_agent[:512] if user_agent else None,
        idempotency_key=idempotency_key,
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)
    return lead


async def update_lead(db: AsyncSession, lead: Lead, payload: LeadUpdate) -> Lead:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    await db.commit()
    await db.refresh(lead)
    return lead


async def count_by_status(db: AsyncSession) -> dict[str, int]:
    result = await db.execute(select(Lead.status, func.count()).group_by(Lead.status))
    counts = {status.value: 0 for status in LeadStatus}
    for status, count in result.all():
        counts[status.value] = count
    return counts
