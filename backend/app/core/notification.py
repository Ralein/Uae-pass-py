from abc import ABC, abstractmethod
import logging

class NotificationProvider(ABC):
    @abstractmethod
    async def send_sms(self, recipient: str, message: str) -> bool:
        pass

    @abstractmethod
    async def send_email(self, recipient: str, subject: str, body: str) -> bool:
        pass

class DevNotificationProvider(NotificationProvider):
    def __init__(self):
        self.logger = logging.getLogger("notification")
        self.logger.setLevel(logging.INFO)

    async def send_sms(self, recipient: str, message: str) -> bool:
        # Log to secure file or stdout in dev
        print(f"========================================")
        print(f"[SMS] To: {recipient}")
        print(f"Message: {message}")
        print(f"========================================")
        self.logger.info(f"SMS to {recipient}: {message}")
        return True

    async def send_email(self, recipient: str, subject: str, body: str) -> bool:
        print(f"========================================")
        print(f"[EMAIL] To: {recipient}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        print(f"========================================")
        self.logger.info(f"Email to {recipient}: {subject}")
        return True

# Factory
def get_notification_provider() -> NotificationProvider:
    # Check settings used ENV
    # if settings.ENV == "PROD": return SMSProvider()
    return DevNotificationProvider()
