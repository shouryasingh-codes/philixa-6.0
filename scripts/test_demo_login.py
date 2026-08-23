import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.database.session import AsyncSessionLocal
from app.api.v1.routes_auth import demo_login
from fastapi import Request, Response
from unittest.mock import MagicMock

async def test_demo_login():
    async with AsyncSessionLocal() as db:
        request = MagicMock(spec=Request)
        request.client.host = "127.0.0.1"
        request.headers = {}
        
        response = Response()
        
        try:
            res = await demo_login(request=request, response=response, db=db)
            print("Success:", res)
        except Exception as e:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_demo_login())
