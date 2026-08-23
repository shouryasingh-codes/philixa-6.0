import asyncio
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from app.database.session import AsyncSessionLocal
from app.models.user import User
from sqlalchemy import select

async def test_delete():
    async with AsyncSessionLocal() as db:
        user = (await db.execute(select(User).limit(1))).scalar_one_or_none()
        if user:
            print(f"Deleting user {user.email}")
            try:
                await db.delete(user)
                await db.commit()
                print("Deleted successfully!")
            except Exception as e:
                print("ERROR:", repr(e))
        else:
            print("No users found")

if __name__ == "__main__":
    asyncio.run(test_delete())
