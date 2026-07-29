import asyncio
from sqlalchemy import text
from app.database.session import AsyncSessionLocal
from app.services.notifications.email_adapter import EmailAdapter
from app.core.config import get_settings

settings = get_settings()

async def test():
    async with AsyncSessionLocal() as db:
        result = await db.execute(text("SELECT whatsapp_number FROM notification_preferences WHERE whatsapp_number IS NOT NULL AND whatsapp_number != '' LIMIT 1;"))
        target_email = result.scalar()
        
        if not target_email:
            print("Bhai, DB me email nahi mili. Pehle UI me save karo!")
            return
            
        print(f"UI me se ye email automatically uthayi: {target_email}")
        
        adapter = EmailAdapter(
            hostname=settings.smtp_hostname,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            use_tls=settings.smtp_use_tls,
            from_address=settings.smtp_from_address
        )
        res = await adapter.send_message(target_email, f"Hello Bhai! System ne UI se tumhara email ({target_email}) khud fetch karke notification bhej diya hai! 🎉")
        print("Email Sent successfully! Details:", res)

if __name__ == "__main__":
    asyncio.run(test())
