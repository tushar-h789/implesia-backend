import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import DbSession, require_editor
from app.schemas.common import Message, Page, PaginationParams
from app.schemas.pricing import (
    EngagementModelCreate,
    EngagementModelRead,
    EngagementModelUpdate,
    PricingPackageCreate,
    PricingPackageRead,
    PricingPackageUpdate,
    PricingPagePublic,
    PricingPageRead,
    PricingPageUpdate,
)
from app.services import pricing_service

public_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(require_editor)])


@public_router.get("", response_model=PricingPagePublic)
async def read_public_pricing(db: DbSession) -> PricingPagePublic:
    page = await pricing_service.get_page(db)
    models = await pricing_service.list_published_models(db)
    packages = await pricing_service.list_published_packages(db)
    body = PricingPagePublic.model_validate(page)
    body.models = [EngagementModelRead.model_validate(item) for item in models]
    body.packages = [PricingPackageRead.model_validate(item) for item in packages]
    return body


@public_router.get("/models/{model_id}", response_model=EngagementModelRead)
async def read_published_model(db: DbSession, model_id: uuid.UUID) -> EngagementModelRead:
    item = await pricing_service.get_model_by_id(db, model_id, published_only=True)
    return EngagementModelRead.model_validate(item)


@public_router.get("/packages/{package_id}", response_model=PricingPackageRead)
async def read_published_package(db: DbSession, package_id: uuid.UUID) -> PricingPackageRead:
    item = await pricing_service.get_package_by_id(db, package_id, published_only=True)
    return PricingPackageRead.model_validate(item)


@admin_router.get("", response_model=PricingPageRead)
async def read_pricing_page(db: DbSession) -> PricingPageRead:
    page = await pricing_service.get_or_create_page(db)
    return PricingPageRead.model_validate(page)


@admin_router.patch("", response_model=PricingPageRead)
async def update_pricing_page(db: DbSession, payload: PricingPageUpdate) -> PricingPageRead:
    page = await pricing_service.get_or_create_page(db)
    updated = await pricing_service.update_page(db, page, payload)
    return PricingPageRead.model_validate(updated)


@admin_router.get("/models", response_model=Page[EngagementModelRead])
async def list_models(
    db: DbSession,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
    published_only: bool = False,
) -> Page[EngagementModelRead]:
    items, total = await pricing_service.list_models(
        db, pagination.offset, pagination.page_size, published_only=published_only, search=search
    )
    return Page[EngagementModelRead](
        items=[EngagementModelRead.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@admin_router.post(
    "/models", response_model=EngagementModelRead, status_code=status.HTTP_201_CREATED
)
async def create_model(db: DbSession, payload: EngagementModelCreate) -> EngagementModelRead:
    item = await pricing_service.create_model(db, payload)
    return EngagementModelRead.model_validate(item)


@admin_router.get("/models/{model_id}", response_model=EngagementModelRead)
async def read_model(db: DbSession, model_id: uuid.UUID) -> EngagementModelRead:
    item = await pricing_service.get_model_by_id(db, model_id)
    return EngagementModelRead.model_validate(item)


@admin_router.patch("/models/{model_id}", response_model=EngagementModelRead)
async def update_model(
    db: DbSession, model_id: uuid.UUID, payload: EngagementModelUpdate
) -> EngagementModelRead:
    item = await pricing_service.get_model_by_id(db, model_id)
    updated = await pricing_service.update_model(db, item, payload)
    return EngagementModelRead.model_validate(updated)


@admin_router.delete("/models/{model_id}", response_model=Message)
async def delete_model(db: DbSession, model_id: uuid.UUID) -> Message:
    item = await pricing_service.get_model_by_id(db, model_id)
    await pricing_service.delete_model(db, item)
    return Message(message="Engagement model deleted")


@admin_router.get("/packages", response_model=Page[PricingPackageRead])
async def list_packages(
    db: DbSession,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
    published_only: bool = False,
) -> Page[PricingPackageRead]:
    items, total = await pricing_service.list_packages(
        db, pagination.offset, pagination.page_size, published_only=published_only, search=search
    )
    return Page[PricingPackageRead](
        items=[PricingPackageRead.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@admin_router.post(
    "/packages", response_model=PricingPackageRead, status_code=status.HTTP_201_CREATED
)
async def create_package(db: DbSession, payload: PricingPackageCreate) -> PricingPackageRead:
    item = await pricing_service.create_package(db, payload)
    return PricingPackageRead.model_validate(item)


@admin_router.get("/packages/{package_id}", response_model=PricingPackageRead)
async def read_package(db: DbSession, package_id: uuid.UUID) -> PricingPackageRead:
    item = await pricing_service.get_package_by_id(db, package_id)
    return PricingPackageRead.model_validate(item)


@admin_router.patch("/packages/{package_id}", response_model=PricingPackageRead)
async def update_package(
    db: DbSession, package_id: uuid.UUID, payload: PricingPackageUpdate
) -> PricingPackageRead:
    item = await pricing_service.get_package_by_id(db, package_id)
    updated = await pricing_service.update_package(db, item, payload)
    return PricingPackageRead.model_validate(updated)


@admin_router.delete("/packages/{package_id}", response_model=Message)
async def delete_package(db: DbSession, package_id: uuid.UUID) -> Message:
    item = await pricing_service.get_package_by_id(db, package_id)
    await pricing_service.delete_package(db, item)
    return Message(message="Pricing package deleted")
