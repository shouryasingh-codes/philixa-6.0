import logging
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.session import get_db
from app.models.notification import NotificationDelivery, DeliveryStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/whatsapp")
async def whatsapp_webhook(
    payload: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Webhook endpoint to receive simulated WhatsApp delivery receipts.
    Expected payload format:
    {
        "provider_message_id": "sim_123456",
        "status": "delivered",
        "error_message": null
    }
    """
    provider_message_id = payload.get("provider_message_id")
    new_status = payload.get("status")
    error_message = payload.get("error_message")

    if not provider_message_id or not new_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing provider_message_id or status in payload"
        )

    # Convert string status to Enum
    try:
        status_enum = DeliveryStatus(new_status.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status value: {new_status}"
        )

    stmt = select(NotificationDelivery).where(
        NotificationDelivery.provider_message_id == provider_message_id
    )
    result = await db.execute(stmt)
    delivery = result.scalar_one_or_none()

    if not delivery:
        # Not found could be normal if it's not ours or out of order
        logger.warning(f"Received webhook for unknown provider_message_id: {provider_message_id}")
        return {"status": "ignored", "detail": "Unknown message ID"}

    # Update delivery status
    delivery.status = status_enum
    if error_message:
        delivery.error_message = error_message

    await db.commit()
    logger.info(f"Updated delivery {delivery.id} to {status_enum}")

    return {"status": "success"}
