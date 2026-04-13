import uuid
from sqlmodel import Session
from app.models.schemas import Notification
from datetime import datetime

class NotificationService:
    @staticmethod
    def send_notification(
        session: Session, 
        worker_id: uuid.UUID, 
        title: str, 
        message: str, 
        msg_type: str = "SYSTEM"
    ) -> Notification:
        """
        Record and 'send' a notification.
        In production, this would dispatch to FCM/Twilio/Email.
        """
        notification = Notification(
            worker_id=worker_id,
            title=title,
            message=message,
            type=msg_type,
            status="SENT",
            created_at=datetime.utcnow()
        )
        session.add(notification)
        session.commit()
        session.refresh(notification)
        
        # Log to console for simulation
        print(f"NOTIFICATION [{msg_type}] to {worker_id}: {title} - {message}")
        
        return notification

    @staticmethod
    def get_user_notifications(session: Session, worker_id: uuid.UUID):
        from sqlmodel import select
        return session.exec(select(Notification).where(Notification.worker_id == worker_id)).all()
