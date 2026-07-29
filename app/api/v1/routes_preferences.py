from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from typing import Any
import uuid

from app.core.security import get_current_org_id
from app.database.session import get_db
from app.models.notification import NotificationPreference
from app.schemas.notification import NotificationPreferenceResponse, NotificationPreferenceUpdate, NotificationPreferenceCreate

router = APIRouter(
    prefix="/preferences",
    tags=["preferences"],
    dependencies=[Depends(get_current_org_id)],
)

@router.get("", response_model=NotificationPreferenceResponse)
async def get_preferences(
    db: AsyncSession = Depends(get_db),
    org_id: str = Depends(get_current_org_id),
) -> Any:
    user_id = "default"
    # First look for a preference with the exact user_id
    pref = await db.scalar(
        select(NotificationPreference).where(
            NotificationPreference.organization_id == org_id,
            NotificationPreference.user_id == user_id
        )
    )
    
    if not pref:
        # If no explicit user_id match, try finding a generic one for the org or create a new one
        pref = NotificationPreference(
            id=str(uuid.uuid4()),
            organization_id=org_id,
            user_id=user_id,
            is_opted_in=True
        )
        db.add(pref)
        await db.commit()
        await db.refresh(pref)
        
    return pref

@router.put("", response_model=NotificationPreferenceResponse)
async def update_preferences(
    preference_update: NotificationPreferenceUpdate,
    db: AsyncSession = Depends(get_db),
    org_id: str = Depends(get_current_org_id),
) -> Any:
    user_id = "default"
    pref = await db.scalar(
        select(NotificationPreference).where(
            NotificationPreference.organization_id == org_id,
            NotificationPreference.user_id == user_id
        )
    )
    
    if not pref:
        # Create it if it doesn't exist
        pref = NotificationPreference(
            id=str(uuid.uuid4()),
            organization_id=org_id,
            user_id=user_id,
        )
        db.add(pref)
    
    update_data = preference_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pref, key, value)
        
    await db.commit()
    await db.refresh(pref)
    return pref
