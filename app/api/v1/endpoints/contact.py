from fastapi import APIRouter, Depends

from app.api.deps import DbSession, require_editor
from app.schemas.contact import ContactPageAdmin, ContactPagePublic, ContactPageUpdate
from app.services import contact_service

public_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(require_editor)])


@public_router.get("", response_model=ContactPagePublic)
async def read_public_contact(db: DbSession) -> ContactPagePublic:
    page = await contact_service.get_page(db)
    return ContactPagePublic.model_validate(page)


@admin_router.get("", response_model=ContactPageAdmin)
async def read_contact_page(db: DbSession) -> ContactPageAdmin:
    page = await contact_service.get_or_create_page(db)
    return ContactPageAdmin.model_validate(page)


@admin_router.patch("", response_model=ContactPageAdmin)
async def update_contact_page(db: DbSession, payload: ContactPageUpdate) -> ContactPageAdmin:
    page = await contact_service.get_or_create_page(db)
    updated = await contact_service.update_page(db, page, payload)
    return ContactPageAdmin.model_validate(updated)
