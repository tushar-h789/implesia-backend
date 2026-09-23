import uuid

from slugify import slugify
from sqlalchemy import ColumnElement, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.order import Order
from app.models.pricing import EngagementModel, PricingPackage, PricingPage
from app.schemas.pricing import (
    EngagementModelCreate,
    EngagementModelUpdate,
    PricingPackageCreate,
    PricingPackageUpdate,
    PricingPageUpdate,
)

DEFAULT_PAGE_SLUG = "pricing"


def _unique_slug(name: str, explicit: str | None) -> str:
    slug = slugify(explicit or name, max_length=180)
    if not slug:
        raise ConflictError("Could not build a URL slug from the name")
    return slug


async def _assert_slug_free(
    db: AsyncSession,
    model: type[EngagementModel] | type[PricingPackage],
    slug: str,
    *,
    exclude_id: uuid.UUID | None = None,
) -> None:
    query = select(model.id).where(model.slug == slug)
    if exclude_id is not None:
        query = query.where(model.id != exclude_id)
    taken = await db.scalar(query)
    if taken is not None:
        raise ConflictError("A record with this slug already exists")


async def get_page(db: AsyncSession, slug: str = DEFAULT_PAGE_SLUG) -> PricingPage:
    result = await db.execute(select(PricingPage).where(PricingPage.slug == slug))
    page = result.scalar_one_or_none()
    if page is None:
        raise NotFoundError("Pricing page not found")
    return page


async def get_or_create_page(db: AsyncSession, slug: str = DEFAULT_PAGE_SLUG) -> PricingPage:
    try:
        return await get_page(db, slug)
    except NotFoundError:
        page = PricingPage(
            slug=slug,
            hero_heading="Clear commercial paths. No guesswork.",
            hero_body=(
                "Choose a custom engagement for product work, or a fixed BDT package "
                "when your brief is already defined. Strategy calls are free either way."
            ),
        )
        db.add(page)
        await db.commit()
        await db.refresh(page)
        return page


async def upsert_page(db: AsyncSession, payload: dict[str, object]) -> PricingPage:
    slug = str(payload.get("slug") or DEFAULT_PAGE_SLUG)
    try:
        page = await get_page(db, slug)
    except NotFoundError:
        page = PricingPage(**payload)
        db.add(page)
        await db.commit()
        await db.refresh(page)
        return page
    for field, value in payload.items():
        setattr(page, field, value)
    await db.commit()
    await db.refresh(page)
    return page


async def update_page(
    db: AsyncSession, page: PricingPage, payload: PricingPageUpdate
) -> PricingPage:
    data = payload.model_dump(mode="json", exclude_unset=True)
    for field, value in data.items():
        setattr(page, field, value)
    await db.commit()
    await db.refresh(page)
    return page


async def get_model_by_id(
    db: AsyncSession, model_id: uuid.UUID, *, published_only: bool = False
) -> EngagementModel:
    item = await db.get(EngagementModel, model_id)
    if item is None or (published_only and not item.is_published):
        raise NotFoundError("Engagement model not found")
    return item


async def get_model_by_slug(
    db: AsyncSession, slug: str, *, published_only: bool = False
) -> EngagementModel:
    query = select(EngagementModel).where(EngagementModel.slug == slug)
    if published_only:
        query = query.where(EngagementModel.is_published.is_(True))
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if item is None:
        raise NotFoundError("Engagement model not found")
    return item


async def get_model_by_ref(
    db: AsyncSession, ref: str, *, published_only: bool = False
) -> EngagementModel:
    try:
        return await get_model_by_id(db, uuid.UUID(ref), published_only=published_only)
    except ValueError:
        return await get_model_by_slug(db, ref, published_only=published_only)


async def list_models(
    db: AsyncSession,
    offset: int,
    limit: int,
    *,
    published_only: bool = False,
    search: str | None = None,
) -> tuple[list[EngagementModel], int]:
    filters: list[ColumnElement[bool]] = []
    if published_only:
        filters.append(EngagementModel.is_published.is_(True))
    if search:
        pattern = f"%{search.lower()}%"
        filters.append(
            or_(
                func.lower(EngagementModel.name).like(pattern),
                func.lower(EngagementModel.slug).like(pattern),
            )
        )
    total = await db.scalar(select(func.count()).select_from(EngagementModel).where(*filters)) or 0
    result = await db.execute(
        select(EngagementModel)
        .where(*filters)
        .order_by(EngagementModel.sort_order.asc(), EngagementModel.name.asc())
        .offset(offset)
        .limit(limit)
    )
    return list(result.scalars().all()), total


async def list_published_models(db: AsyncSession) -> list[EngagementModel]:
    items, _ = await list_models(db, 0, 100, published_only=True)
    return items


async def create_model(db: AsyncSession, payload: EngagementModelCreate) -> EngagementModel:
    slug = _unique_slug(payload.name, payload.slug)
    await _assert_slug_free(db, EngagementModel, slug)
    data = payload.model_dump(mode="json")
    data["slug"] = slug
    item = EngagementModel(**data)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def update_model(
    db: AsyncSession, item: EngagementModel, payload: EngagementModelUpdate
) -> EngagementModel:
    data = payload.model_dump(mode="json", exclude_unset=True)
    if "slug" in data:
        new_slug = _unique_slug(data.get("name", item.name), data["slug"])
        await _assert_slug_free(db, EngagementModel, new_slug, exclude_id=item.id)
        data["slug"] = new_slug
    for field, value in data.items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


async def delete_model(db: AsyncSession, item: EngagementModel) -> None:
    order_count = await db.scalar(
        select(func.count()).select_from(Order).where(Order.model_id == item.id)
    )
    if order_count:
        raise ConflictError("This model has orders. Cancel or reassign them before deleting.")
    await db.delete(item)
    await db.commit()


async def get_package_by_id(
    db: AsyncSession, package_id: uuid.UUID, *, published_only: bool = False
) -> PricingPackage:
    item = await db.get(PricingPackage, package_id)
    if item is None or (published_only and not item.is_published):
        raise NotFoundError("Pricing package not found")
    return item


async def get_package_by_slug(
    db: AsyncSession, slug: str, *, published_only: bool = False
) -> PricingPackage:
    query = select(PricingPackage).where(PricingPackage.slug == slug)
    if published_only:
        query = query.where(PricingPackage.is_published.is_(True))
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if item is None:
        raise NotFoundError("Pricing package not found")
    return item


async def get_package_by_ref(
    db: AsyncSession, ref: str, *, published_only: bool = False
) -> PricingPackage:
    try:
        return await get_package_by_id(db, uuid.UUID(ref), published_only=published_only)
    except ValueError:
        return await get_package_by_slug(db, ref, published_only=published_only)


async def list_packages(
    db: AsyncSession,
    offset: int,
    limit: int,
    *,
    published_only: bool = False,
    search: str | None = None,
) -> tuple[list[PricingPackage], int]:
    filters: list[ColumnElement[bool]] = []
    if published_only:
        filters.append(PricingPackage.is_published.is_(True))
    if search:
        pattern = f"%{search.lower()}%"
        filters.append(
            or_(
                func.lower(PricingPackage.name).like(pattern),
                func.lower(PricingPackage.slug).like(pattern),
            )
        )
    total = await db.scalar(select(func.count()).select_from(PricingPackage).where(*filters)) or 0
    result = await db.execute(
        select(PricingPackage)
        .where(*filters)
        .order_by(PricingPackage.sort_order.asc(), PricingPackage.name.asc())
        .offset(offset)
        .limit(limit)
    )
    return list(result.scalars().all()), total


async def list_published_packages(db: AsyncSession) -> list[PricingPackage]:
    items, _ = await list_packages(db, 0, 100, published_only=True)
    return items


async def create_package(db: AsyncSession, payload: PricingPackageCreate) -> PricingPackage:
    slug = _unique_slug(payload.name, payload.slug)
    await _assert_slug_free(db, PricingPackage, slug)
    data = payload.model_dump(mode="json")
    data["slug"] = slug
    if not data.get("cta_label"):
        data["cta_label"] = f"Enquire about {payload.name}"
    item = PricingPackage(**data)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def update_package(
    db: AsyncSession, item: PricingPackage, payload: PricingPackageUpdate
) -> PricingPackage:
    data = payload.model_dump(mode="json", exclude_unset=True)
    if "slug" in data:
        new_slug = _unique_slug(data.get("name", item.name), data["slug"])
        await _assert_slug_free(db, PricingPackage, new_slug, exclude_id=item.id)
        data["slug"] = new_slug
    for field, value in data.items():
        setattr(item, field, value)
    await db.commit()
    await db.refresh(item)
    return item


async def delete_package(db: AsyncSession, item: PricingPackage) -> None:
    order_count = await db.scalar(
        select(func.count()).select_from(Order).where(Order.package_id == item.id)
    )
    if order_count:
        raise ConflictError("This package has orders. Cancel or reassign them before deleting.")
    await db.delete(item)
    await db.commit()
