from fastapi import APIRouter, Depends

from app.api.deps import DbSession, require_editor
from app.schemas.about import AboutPageAdmin, AboutPagePublic, AboutPageUpdate
from app.services import about_service

public_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(require_editor)])


@public_router.get("", response_model=AboutPagePublic)
async def read_public_about(db: DbSession) -> AboutPagePublic:
    page = await about_service.get_page(db)
    return AboutPagePublic.model_validate(page)


@admin_router.get("", response_model=AboutPageAdmin)
async def read_about_page(db: DbSession) -> AboutPageAdmin:
    page = await about_service.get_or_create_page(db)
    return AboutPageAdmin.model_validate(page)


@admin_router.patch("", response_model=AboutPageAdmin)
async def update_about_page(db: DbSession, payload: AboutPageUpdate) -> AboutPageAdmin:
    page = await about_service.get_or_create_page(db)
    updated = await about_service.update_page(db, page, payload)
    return AboutPageAdmin.model_validate(updated)
