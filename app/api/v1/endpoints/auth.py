from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.database import get_session
from app.schemas.api import OTPRequest, OTPVerify, Token
from app.services.auth import AuthService, create_access_token
from app.models.schemas import Worker

router = APIRouter()

@router.post("/otp/send")
def send_otp(payload: OTPRequest):
    AuthService.send_otp(payload.phone)
    return {"message": "OTP sent successfully"}

@router.post("/otp/verify", response_model=Token)
def verify_otp(payload: OTPVerify, session: Session = Depends(get_session)):
    if not AuthService.verify_otp(payload.phone, payload.otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Get or create worker
    worker = session.exec(select(Worker).where(Worker.phone == payload.phone)).first()
    if not worker:
        worker = Worker(phone=payload.phone)
        session.add(worker)
        session.commit()
        session.refresh(worker)
    
    access_token = create_access_token(data={"sub": worker.phone})
    return {
        "access_token": access_token,
        "refresh_token": "mock_refresh_token",
        "user_id": str(worker.id)
    }

@router.get("/validate")
def validate_token():
    return {"status": "valid"}

@router.post("/logout")
def logout():
    return {"message": "Logged out"}
