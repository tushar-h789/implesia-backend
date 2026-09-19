from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.contact import ContactPage
from app.schemas.contact import ContactPageUpdate

DEFAULT_PAGE_SLUG = "contact"


async def get_page(db: AsyncSession, slug: str = DEFAULT_PAGE_SLUG) -> ContactPage:
    result = await db.execute(select(ContactPage).where(ContactPage.slug == slug))
    page = result.scalar_one_or_none()
    if page is None:
        raise NotFoundError("Contact page not found")
    return page


async def get_or_create_page(db: AsyncSession, slug: str = DEFAULT_PAGE_SLUG) -> ContactPage:
    try:
        return await get_page(db, slug)
    except NotFoundError:
        page = ContactPage(
            slug=slug,
            hero_heading="Tell us about your project.",
            hero_body=(
                "Whether you have a defined brief or an early-stage idea, our team "
                "will assess your requirements and respond with a clear path forward."
            ),
        )
        db.add(page)
        await db.commit()
        await db.refresh(page)
        return page


async def upsert_page(db: AsyncSession, payload: dict[str, object]) -> ContactPage:
    slug = str(payload.get("slug") or DEFAULT_PAGE_SLUG)
    try:
        page = await get_page(db, slug)
    except NotFoundError:
        page = ContactPage(**payload)
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
    db: AsyncSession, page: ContactPage, payload: ContactPageUpdate
) -> ContactPage:
    data = payload.model_dump(mode="json", exclude_unset=True)
    for field, value in data.items():
        setattr(page, field, value)
    await db.commit()
    await db.refresh(page)
    return page
