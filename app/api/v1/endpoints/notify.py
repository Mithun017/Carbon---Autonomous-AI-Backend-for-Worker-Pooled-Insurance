from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.notification_service import NotificationService
from app.schemas.api import (
    BaseResponse, NotificationSendRequest, NotificationSendData,
    NotificationRetryRequest, NotificationRetryData
)
from typing import List, Any
from uuid import UUID

router = APIRouter()

@router.get("/{user_id}", response_model=BaseResponse[List[Any]])
def get_notifications(user_id: UUID, session: Session = Depends(get_session)):
    notifications = NotificationService.get_user_notifications(session, user_id)
    return BaseResponse(data=notifications)

@router.post("/send", response_model=BaseResponse[NotificationSendData])
def send_manual_notification(payload: NotificationSendRequest, session: Session = Depends(get_session)):
    # Contract: message, user_id, Response: sent
    NotificationService.send_notification(session, UUID(payload.user_id), "Admin Notification", payload.message)
    return BaseResponse(data=NotificationSendData(sent=True))

@router.post("/retry", response_model=BaseResponse[NotificationRetryData])
def retry_notification(payload: NotificationRetryRequest):
    return BaseResponse(data=NotificationRetryData(retried=True))
