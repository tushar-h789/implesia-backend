"""Create the bootstrap admin and seed catalogue rows if the database is empty."""

import asyncio

from sqlalchemy import func, select

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.service import Service
from scripts.create_superuser import main as create_superuser
from scripts.seed_about import main as seed_about
from scripts.seed_articles import main as seed_articles
from scripts.seed_contact import main as seed_contact
from scripts.seed_portfolio import main as seed_portfolio
from scripts.seed_pricing import main as seed_pricing
from scripts.seed_services import main as seed_services
from scripts.seed_team import main as seed_team


async def main() -> None:
    await create_superuser(
        settings.first_superuser_email,
        settings.first_superuser_password,
        "Implesia Admin",
    )
    async with SessionLocal() as db:
        count = await db.scalar(select(func.count()).select_from(Service))
    if count:
        print(f"Catalogue already has {count} services; skipping seed.")
        return
    print("Empty catalogue — seeding CMS pages.")
    await seed_services()
    await seed_pricing()
    await seed_portfolio()
    await seed_articles()
    await seed_about()
    await seed_team()
    await seed_contact()
    print("Production bootstrap complete.")


if __name__ == "__main__":
    asyncio.run(main())
