import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import DbSession, require_editor
from app.schemas.common import Message, Page, PaginationParams
from app.schemas.service import ServiceCreate, ServiceRead, ServiceUpdate
from app.services import service_service

public_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(require_editor)])


@public_router.get("", response_model=Page[ServiceRead])
async def list_published_services(
    db: DbSession,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
) -> Page[ServiceRead]:
    items, total = await service_service.list_services(
        db, pagination.offset, pagination.page_size, published_only=True, search=search
    )
    return Page[ServiceRead](
        items=[ServiceRead.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@public_router.get("/{service_id}", response_model=ServiceRead)
async def read_published_service(db: DbSession, service_id: uuid.UUID) -> ServiceRead:
    service = await service_service.get_by_id(db, service_id, published_only=True)
    return ServiceRead.model_validate(service)


@admin_router.get("", response_model=Page[ServiceRead])
async def list_services(
    db: DbSession,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
    published_only: bool = False,
) -> Page[ServiceRead]:
    items, total = await service_service.list_services(
        db,
        pagination.offset,
        pagination.page_size,
        published_only=published_only,
        search=search,
    )
    return Page[ServiceRead](
        items=[ServiceRead.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@admin_router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
async def create_service(db: DbSession, payload: ServiceCreate) -> ServiceRead:
    service = await service_service.create_service(db, payload)
    return ServiceRead.model_validate(service)


@admin_router.get("/{service_id}", response_model=ServiceRead)
async def read_service(db: DbSession, service_id: uuid.UUID) -> ServiceRead:
    service = await service_service.get_by_id(db, service_id)
    return ServiceRead.model_validate(service)


@admin_router.patch("/{service_id}", response_model=ServiceRead)
async def update_service(
    db: DbSession, service_id: uuid.UUID, payload: ServiceUpdate
) -> ServiceRead:
    service = await service_service.get_by_id(db, service_id)
    updated = await service_service.update_service(db, service, payload)
    return ServiceRead.model_validate(updated)


@admin_router.delete("/{service_id}", response_model=Message)
async def delete_service(db: DbSession, service_id: uuid.UUID) -> Message:
    service = await service_service.get_by_id(db, service_id)
    await service_service.delete_service(db, service)
    return Message(message="Service deleted")
