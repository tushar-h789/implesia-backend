from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import DbSession, require_editor
from app.schemas.common import Message, Page, PaginationParams
from app.schemas.team import (
    TeamMemberAdmin,
    TeamMemberCreate,
    TeamMemberPublic,
    TeamMemberUpdate,
    TeamPagePublic,
    TeamPageRead,
    TeamPageUpdate,
)
from app.services import team_service

public_router = APIRouter()
admin_router = APIRouter(dependencies=[Depends(require_editor)])


@public_router.get("", response_model=TeamPagePublic)
async def read_public_team(db: DbSession) -> TeamPagePublic:
    page = await team_service.get_page(db)
    featured = await team_service.get_featured_member(db)
    members = await team_service.list_published_members(db)
    body = TeamPagePublic.model_validate(page)
    body.featured = TeamMemberPublic.model_validate(featured) if featured is not None else None
    body.members = [TeamMemberPublic.model_validate(item) for item in members]
    return body


@public_router.get("/members/{slug}", response_model=TeamMemberPublic)
async def read_published_member(db: DbSession, slug: str) -> TeamMemberPublic:
    item = await team_service.get_member_by_slug(db, slug, published_only=True)
    return TeamMemberPublic.model_validate(item)


@admin_router.get("", response_model=TeamPageRead)
async def read_team_page(db: DbSession) -> TeamPageRead:
    page = await team_service.get_or_create_page(db)
    return TeamPageRead.model_validate(page)


@admin_router.patch("", response_model=TeamPageRead)
async def update_team_page(db: DbSession, payload: TeamPageUpdate) -> TeamPageRead:
    page = await team_service.get_or_create_page(db)
    updated = await team_service.update_page(db, page, payload)
    return TeamPageRead.model_validate(updated)


@admin_router.get("/members", response_model=Page[TeamMemberAdmin])
async def list_members(
    db: DbSession,
    pagination: Annotated[PaginationParams, Depends()],
    search: str | None = None,
    published_only: bool = False,
) -> Page[TeamMemberAdmin]:
    items, total = await team_service.list_members(
        db,
        pagination.offset,
        pagination.page_size,
        published_only=published_only,
        search=search,
    )
    return Page[TeamMemberAdmin](
        items=[TeamMemberAdmin.model_validate(item) for item in items],
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
    )


@admin_router.post("/members", response_model=TeamMemberAdmin, status_code=status.HTTP_201_CREATED)
async def create_member(db: DbSession, payload: TeamMemberCreate) -> TeamMemberAdmin:
    item = await team_service.create_member(db, payload)
    return TeamMemberAdmin.model_validate(item)


@admin_router.get("/members/{member_ref}", response_model=TeamMemberAdmin)
async def read_member(db: DbSession, member_ref: str) -> TeamMemberAdmin:
    item = await team_service.get_member_by_ref(db, member_ref)
    return TeamMemberAdmin.model_validate(item)


@admin_router.patch("/members/{member_ref}", response_model=TeamMemberAdmin)
async def update_member(
    db: DbSession, member_ref: str, payload: TeamMemberUpdate
) -> TeamMemberAdmin:
    item = await team_service.get_member_by_ref(db, member_ref)
    updated = await team_service.update_member(db, item, payload)
    return TeamMemberAdmin.model_validate(updated)


@admin_router.delete("/members/{member_ref}", response_model=Message)
async def delete_member(db: DbSession, member_ref: str) -> Message:
    item = await team_service.get_member_by_ref(db, member_ref)
    await team_service.delete_member(db, item)
    return Message(message="Team member deleted")
