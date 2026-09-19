import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import DbSession, require_editor
from app.schemas.common import Message, Page, PaginationParams
from app.schemas.portfolio import (
    PortfolioPagePublic,
    PortfolioPageRead,
    PortfolioPageUpdate,
    PortfolioProjectAdmin,
    PortfolioProjectCreate,
    PortfolioProjectPublic,
    PortfolioProjectUpdate,
)
from app.services import portfolio_service

public_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(require_editor)])


@public_router.get("", response_model=PortfolioPagePublic)
async def read_public_portfolio(db: DbSession, category: str | None = None) -> PortfolioPagePublic:
    page = await portfolio_service.get_page(db)
    featured = await portfolio_service.get_featured_project(db)
    projects = await portfolio_service.list_published_projects(db, category=category)
    body = PortfolioPagePublic.model_validate(page)
    body.featured = (
        PortfolioProjectPublic.model_validate(featured) if featured is not None else None
    )
    body.projects = [PortfolioProjectPublic.model_validate(item) for item in projects]
    return body


@public_router.get("/projects/{project_id}", response_model=PortfolioProjectPublic)
async def read_published_project(db: DbSession, project_id: uuid.UUID) -> PortfolioProjectPublic:
    item = await portfolio_service.get_project_by_id(db, project_id, published_only=True)
    return PortfolioProjectPublic.model_validate(item)


@admin_router.get("", response_model=PortfolioPageRead)
async def read_portfolio_page(db: DbSession) -> PortfolioPageRead:
    page = await portfolio_service.get_or_create_page(db)
    return PortfolioPageRead.model_validate(page)


@admin_router.patch("", response_model=PortfolioPageRead)
async def update_portfolio_page(db: DbSession, payload: PortfolioPageUpdate) -> PortfolioPageRead:
    page = await portfolio_service.get_or_create_page(db)
    updated = await portfolio_service.update_page(db, page, payload)
    return PortfolioPageRead.model_validate(updated)


@admin_router.get("/projects", response_model=Page[PortfolioProjectAdmin])
async def list_projects(
    db: DbSession,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
    category: str | None = None,
    published_only: bool = False,
) -> Page[PortfolioProjectAdmin]:
    items, total = await portfolio_service.list_projects(
        db,
        pagination.offset,
        pagination.page_size,
        published_only=published_only,
        search=search,
        category=category,
    )
    return Page[PortfolioProjectAdmin](
        items=[PortfolioProjectAdmin.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@admin_router.post(
    "/projects",
    response_model=PortfolioProjectAdmin,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(db: DbSession, payload: PortfolioProjectCreate) -> PortfolioProjectAdmin:
    item = await portfolio_service.create_project(db, payload)
    return PortfolioProjectAdmin.model_validate(item)


@admin_router.get("/projects/{project_id}", response_model=PortfolioProjectAdmin)
async def read_project(db: DbSession, project_id: uuid.UUID) -> PortfolioProjectAdmin:
    item = await portfolio_service.get_project_by_id(db, project_id)
    return PortfolioProjectAdmin.model_validate(item)


@admin_router.patch("/projects/{project_id}", response_model=PortfolioProjectAdmin)
async def update_project(
    db: DbSession, project_id: uuid.UUID, payload: PortfolioProjectUpdate
) -> PortfolioProjectAdmin:
    item = await portfolio_service.get_project_by_id(db, project_id)
    updated = await portfolio_service.update_project(db, item, payload)
    return PortfolioProjectAdmin.model_validate(updated)


@admin_router.delete("/projects/{project_id}", response_model=Message)
async def delete_project(db: DbSession, project_id: uuid.UUID) -> Message:
    item = await portfolio_service.get_project_by_id(db, project_id)
    await portfolio_service.delete_project(db, item)
    return Message(message="Portfolio project deleted")
