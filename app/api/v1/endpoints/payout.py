from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.payout_service import PayoutService
import uuid

router = APIRouter()

@router.post("/process")
def process_payout(claim_id: uuid.UUID, worker_id: uuid.UUID, amount: float, session: Session = Depends(get_session)):
    try:
        payout = PayoutService.process_payout(session, claim_id, worker_id, amount)
        return payout
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}")
def get_user_payouts(user_id: uuid.UUID, session: Session = Depends(get_session)):
    return PayoutService.get_user_payouts(session, user_id)

@router.post("/retry")
def retry_payout(payout_id: uuid.UUID, session: Session = Depends(get_session)):
    # Mock retry logic
    return {"message": f"Retry initiated for payout {payout_id}"}
