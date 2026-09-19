from fastapi import APIRouter

from app.api.v1.endpoints import (
    about,
    articles,
    auth,
    contact,
    leads,
    orders,
    portfolio,
    pricing,
    services,
    team,
    users,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(leads.public_router, prefix="/leads", tags=["leads"])
api_router.include_router(leads.admin_router, prefix="/admin/leads", tags=["admin:leads"])
api_router.include_router(services.public_router, prefix="/services", tags=["services"])
api_router.include_router(services.admin_router, prefix="/admin/services", tags=["admin:services"])
api_router.include_router(orders.public_router, prefix="/orders", tags=["orders"])
api_router.include_router(orders.admin_router, prefix="/admin/orders", tags=["admin:orders"])
api_router.include_router(pricing.public_router, prefix="/pricing", tags=["pricing"])
api_router.include_router(pricing.admin_router, prefix="/admin/pricing", tags=["admin:pricing"])
api_router.include_router(portfolio.public_router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(
    portfolio.admin_router, prefix="/admin/portfolio", tags=["admin:portfolio"]
)
api_router.include_router(articles.public_router, prefix="/articles", tags=["articles"])
api_router.include_router(articles.admin_router, prefix="/admin/articles", tags=["admin:articles"])
api_router.include_router(about.public_router, prefix="/about-us", tags=["about"])
api_router.include_router(about.admin_router, prefix="/admin/about-us", tags=["admin:about"])
api_router.include_router(team.public_router, prefix="/team", tags=["team"])
api_router.include_router(team.admin_router, prefix="/admin/team", tags=["admin:team"])
api_router.include_router(contact.public_router, prefix="/contact", tags=["contact"])
api_router.include_router(contact.admin_router, prefix="/admin/contact", tags=["admin:contact"])
