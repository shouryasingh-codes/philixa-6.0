import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.session import AsyncSessionLocal
from app.services.portfolio_copilot_service import process_copilot_query

async def main():
    async with AsyncSessionLocal() as db:
        res = await process_copilot_query('राजेश शर्मा के बारे में बताओ', 'org1', 'user1', 'admin', db, client_name='Rajesh Sharma')
        print(res)

asyncio.run(main())
