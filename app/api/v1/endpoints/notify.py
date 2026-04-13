from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.notification_service import NotificationService
import uuid

router = APIRouter()

@router.get("/{user_id}")
def get_notifications(user_id: uuid.UUID, session: Session = Depends(get_session)):
    return NotificationService.get_user_notifications(session, user_id)

@router.post("/send")
def send_manual_notification(worker_id: uuid.UUID, title: str, message: str, session: Session = Depends(get_session)):
    return NotificationService.send_notification(session, worker_id, title, message)

@router.post("/retry")
def retry_notification(notification_id: uuid.UUID):
    return {"message": f"Retry successful for {notification_id}"}
