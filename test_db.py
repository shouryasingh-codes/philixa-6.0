import asyncio
from app.database.session import AsyncSessionLocal
from app.models.client import Client
from sqlalchemy import select

async def main():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Client))
        clients = res.scalars().all()
        for c in clients:
            print(f"ID: {c.id}, Name: '{c.name}', Org: {c.organization_id}")

asyncio.run(main())
