import uuid

from slugify import slugify
from sqlalchemy import ColumnElement, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.order import Order
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceUpdate


def _unique_slug(name: str, explicit: str | None) -> str:
    slug = slugify(explicit or name, max_length=180)
    if not slug:
        raise ConflictError("Could not build a URL slug from the service name")
    return slug


async def get_by_id(
    db: AsyncSession, service_id: uuid.UUID, *, published_only: bool = False
) -> Service:
    service = await db.get(Service, service_id)
    if service is None or (published_only and not service.is_published):
        raise NotFoundError("Service not found")
    return service


async def get_by_ref(db: AsyncSession, ref: str, *, published_only: bool = False) -> Service:
    """Resolve a service by UUID or slug so admin and Bruno URLs stay usable."""
    try:
        return await get_by_id(db, uuid.UUID(ref), published_only=published_only)
    except ValueError:
        return await get_by_slug(db, ref, published_only=published_only)


async def get_by_slug(db: AsyncSession, slug: str, *, published_only: bool = False) -> Service:
    query = select(Service).where(Service.slug == slug)
    if published_only:
        query = query.where(Service.is_published.is_(True))
    result = await db.execute(query)
    service = result.scalar_one_or_none()
    if service is None:
        raise NotFoundError("Service not found")
    return service


async def list_services(
    db: AsyncSession,
    offset: int,
    limit: int,
    *,
    published_only: bool = False,
    search: str | None = None,
) -> tuple[list[Service], int]:
    filters: list[ColumnElement[bool]] = []
    if published_only:
        filters.append(Service.is_published.is_(True))
    if search:
        pattern = f"%{search.lower()}%"
        filters.append(
            or_(
                func.lower(Service.name).like(pattern),
                func.lower(Service.slug).like(pattern),
                func.lower(Service.category).like(pattern),
            )
        )

    total = await db.scalar(select(func.count()).select_from(Service).where(*filters)) or 0
    result = await db.execute(
        select(Service)
        .where(*filters)
        .order_by(Service.sort_order.asc(), Service.name.asc())
        .offset(offset)
        .limit(limit)
    )
    return list(result.scalars().all()), total


async def _assert_slug_free(
    db: AsyncSession, slug: str, *, exclude_id: uuid.UUID | None = None
) -> None:
    query = select(Service.id).where(Service.slug == slug)
    if exclude_id is not None:
        query = query.where(Service.id != exclude_id)
    taken = await db.scalar(query)
    if taken is not None:
        raise ConflictError("A service with this slug already exists")


async def create_service(db: AsyncSession, payload: ServiceCreate) -> Service:
    slug = _unique_slug(payload.name, payload.slug)
    await _assert_slug_free(db, slug)
    data = payload.model_dump(mode="json")
    data["slug"] = slug
    service = Service(**data)
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return service


async def update_service(db: AsyncSession, service: Service, payload: ServiceUpdate) -> Service:
    data = payload.model_dump(mode="json", exclude_unset=True)
    if "slug" in data:
        new_slug = _unique_slug(data.get("name", service.name), data["slug"])
        await _assert_slug_free(db, new_slug, exclude_id=service.id)
        data["slug"] = new_slug
    for field, value in data.items():
        setattr(service, field, value)
    await db.commit()
    await db.refresh(service)
    return service


async def delete_service(db: AsyncSession, service: Service) -> None:
    order_count = await db.scalar(
        select(func.count()).select_from(Order).where(Order.service_id == service.id)
    )
    if order_count:
        raise ConflictError("This service has orders. Cancel or reassign them before deleting.")
    await db.delete(service)
    await db.commit()
