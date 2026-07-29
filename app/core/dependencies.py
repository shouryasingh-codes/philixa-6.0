from typing import Optional
from app.core.config import get_settings
from app.services.notifications.base import NotificationAdapter
from app.services.notifications.simulator import SimulatedNotificationAdapter
from app.services.notifications.email_adapter import EmailAdapter

_notification_adapter: Optional[NotificationAdapter] = None

def get_notification_adapter() -> NotificationAdapter:
    """
    Dependency to inject the NotificationAdapter into routes or services.
    Returns the appropriate adapter based on settings.
    """
    global _notification_adapter
    if _notification_adapter is not None:
        return _notification_adapter
        
    settings = get_settings()
    
    if settings.notification_mode == "email":
        _notification_adapter = EmailAdapter(
            hostname=settings.smtp_hostname,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            use_tls=settings.smtp_use_tls,
            from_address=settings.smtp_from_address
        )
    else:
        _notification_adapter = SimulatedNotificationAdapter()
        
    return _notification_adapter
