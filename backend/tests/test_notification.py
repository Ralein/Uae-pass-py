import pytest
from app.core.notification import get_notification_provider, DevNotificationProvider

@pytest.mark.asyncio
async def test_notification_provider():
    provider = get_notification_provider()
    assert isinstance(provider, DevNotificationProvider)
    
    sent = await provider.send_sms("+971500000000", "Test Message")
    assert sent is True
    
    sent_email = await provider.send_email("test@example.com", "Subject", "Body")
    assert sent_email is True
