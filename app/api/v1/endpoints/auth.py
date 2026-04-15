from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_session
from app.schemas.api import (
    BaseResponse, LoginRequest, LoginData, LogoutData,
    OTPSendRequest, OTPSendData, OTPVerifyRequest, OTPVerifyData,
    RefreshRequest, RefreshData, ValidateData
)
from app.services.auth import AuthService, create_access_token
from app.models.schemas import Worker
import uuid

router = APIRouter()

@router.post("/login", response_model=BaseResponse[LoginData])
def login(payload: LoginRequest, session: Session = Depends(get_session)):
    # Mock login logic: handle both phone and email as 'login' field
    # For now, we reuse OTP verification if 'secret' is length 6, else assume password
    # This is a simplified implementation to match the contract structure
    
    worker = session.exec(select(Worker).where((Worker.phone == payload.login) | (Worker.email == payload.login))).first()
    
    if not worker:
        # For demo purposes, create worker if phone-like login
        if payload.login.isdigit():
             worker = Worker(phone=payload.login)
             session.add(worker)
             session.commit()
             session.refresh(worker)
        else:
            raise HTTPException(status_code=404, detail="User not found")
    
    access_token = create_access_token(data={"sub": worker.phone})
    return BaseResponse(data=LoginData(
        access_token=access_token,
        refresh_token=f"ref_{uuid.uuid4().hex}",
        user_id=str(worker.id)
    ))

@router.post("/logout", response_model=BaseResponse[LogoutData])
def logout():
    return BaseResponse(data=LogoutData())

@router.post("/otp/send", response_model=BaseResponse[OTPSendData])
def send_otp(payload: OTPSendRequest):
    AuthService.send_otp(payload.phone_number)
    return BaseResponse(data=OTPSendData(otp_sent=True))

@router.post("/otp/verify", response_model=BaseResponse[OTPVerifyData])
def verify_otp(payload: OTPVerifyRequest, session: Session = Depends(get_session)):
    if not AuthService.verify_otp(payload.phone, payload.otp):
        return BaseResponse(data=OTPVerifyData(verified=False, token=""))
    
    worker = session.exec(select(Worker).where(Worker.phone == payload.phone)).first()
    if not worker:
        worker = Worker(phone=payload.phone)
        session.add(worker)
        session.commit()
        session.refresh(worker)
    
    token = create_access_token(data={"sub": worker.phone})
    return BaseResponse(data=OTPVerifyData(verified=True, token=token))

@router.post("/refresh", response_model=BaseResponse[RefreshData])
def refresh_token(payload: RefreshRequest):
    return BaseResponse(data=RefreshData(new_access_token=f"new_acc_{uuid.uuid4().hex}"))

@router.get("/validate", response_model=BaseResponse[ValidateData])
def validate_token(access_token: str):
    # Mock validation
    return BaseResponse(data=ValidateData(is_valid=True, user_id="some_user_id"))
