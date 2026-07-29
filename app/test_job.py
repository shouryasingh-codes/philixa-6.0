import asyncio
from app.jobs.notification_jobs import send_pre_interaction_briefs
from app.database.session import AsyncSessionLocal
import app.models  # Ensure all models are registered

async def run():
    ctx = {"db_session_factory": AsyncSessionLocal}
    print("Triggering send_pre_interaction_briefs manually...")
    await send_pre_interaction_briefs(ctx)
    print("Job completed!")

if __name__ == "__main__":
    asyncio.run(run())
