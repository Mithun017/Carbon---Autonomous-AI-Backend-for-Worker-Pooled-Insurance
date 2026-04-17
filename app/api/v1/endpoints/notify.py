from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.notification_service import NotificationService
from app.schemas.api import (
    BaseResponse, NotificationSendRequest, NotificationSendData,
    NotificationRetryRequest, NotificationRetryData, NotificationData
)
from app.models.schemas import Notification
from typing import List, Any
from uuid import UUID

router = APIRouter()

@router.get("/{user_id}", response_model=BaseResponse[List[NotificationData]])
def get_user_notifications(user_id: UUID, session: Session = Depends(get_session)):
    from sqlmodel import select
    notifications = session.exec(select(Notification).where(Notification.worker_id == user_id).order_by(Notification.created_at.desc())).all()
    data = [
        NotificationData(
            notification_id=str(n.id),
            message=n.message,
            sent_at=n.created_at.isoformat(),
            status=n.status.lower()
        ) for n in notifications
    ]
    return BaseResponse(data=data)

@router.post("/send", response_model=BaseResponse[NotificationSendData])
def send_manual_notification(payload: NotificationSendRequest, session: Session = Depends(get_session)):
    # Contract 11.2: message, user_id, Response: sent
    NotificationService.send_notification(session, UUID(payload.user_id), "Admin Notification", payload.message)
    return BaseResponse(data=NotificationSendData(sent=True))

@router.post("/retry", response_model=BaseResponse[NotificationRetryData])
def retry_notification(payload: NotificationRetryRequest):
    return BaseResponse(data=NotificationRetryData(retried=True))
