from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.about import AboutPage
from app.schemas.about import AboutPageUpdate

DEFAULT_PAGE_SLUG = "about-us"


async def get_page(db: AsyncSession, slug: str = DEFAULT_PAGE_SLUG) -> AboutPage:
    result = await db.execute(select(AboutPage).where(AboutPage.slug == slug))
    page = result.scalar_one_or_none()
    if page is None:
        raise NotFoundError("About page not found")
    return page


async def get_or_create_page(db: AsyncSession, slug: str = DEFAULT_PAGE_SLUG) -> AboutPage:
    try:
        return await get_page(db, slug)
    except NotFoundError:
        page = AboutPage(
            slug=slug,
            hero_heading="Engineering platforms that perform under pressure.",
            hero_body=(
                "Implesia IT is a software engineering partner for organisations "
                "that treat uptime, security, and maintainability as business "
                "priorities—not afterthoughts."
            ),
        )
        db.add(page)
        await db.commit()
        await db.refresh(page)
        return page


async def upsert_page(db: AsyncSession, payload: dict[str, object]) -> AboutPage:
    slug = str(payload.get("slug") or DEFAULT_PAGE_SLUG)
    try:
        page = await get_page(db, slug)
    except NotFoundError:
        page = AboutPage(**payload)
        db.add(page)
        await db.commit()
        await db.refresh(page)
        return page
    for field, value in payload.items():
        setattr(page, field, value)
    await db.commit()
    await db.refresh(page)
    return page


async def update_page(db: AsyncSession, page: AboutPage, payload: AboutPageUpdate) -> AboutPage:
    data = payload.model_dump(mode="json", exclude_unset=True)
    for field, value in data.items():
        setattr(page, field, value)
    await db.commit()
    await db.refresh(page)
    return page
