from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.payout_service import PayoutService
from app.schemas.api import (
    BaseResponse, PayoutData, PayoutProcessRequest, PayoutProcessData,
    PayoutRetryRequest, PayoutRetryData
)
from typing import List, Any
from uuid import UUID

router = APIRouter()

@router.get("/{user_id}", response_model=BaseResponse[List[PayoutData]])
def get_user_payouts(user_id: UUID, session: Session = Depends(get_session)):
    # Contract 10.1: payout_id, claim_id, amount, status, paid_at
    payouts = PayoutService.get_user_payouts(session, user_id)
    data = [
        PayoutData(
            payout_id=str(p.id),
            claim_id=str(p.claim_id),
            amount=p.amount,
            status=p.status.lower(),
            paid_at=p.created_at.isoformat() if p.created_at else None
        ) for p in payouts
    ]
    return BaseResponse(data=data)

@router.post("/process", response_model=BaseResponse[PayoutProcessData])
def process_payout(payload: PayoutProcessRequest, session: Session = Depends(get_session)):
    # Contract 10.2: payout_id, amount, status
    from app.models.schemas import Claim
    claim = session.get(Claim, UUID(payload.claim_id))
    if not claim:
         raise HTTPException(status_code=404, detail="Claim not found")
         
    try:
        payout = PayoutService.process_payout(session, claim.id, claim.worker_id, claim.amount)
        return BaseResponse(data=PayoutProcessData(
            payout_id=str(payout.id),
            amount=payout.amount,
            status=payout.status.lower()
        ))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/retry", response_model=BaseResponse[PayoutRetryData])
def retry_payout(payload: PayoutRetryRequest, session: Session = Depends(get_session)):
    # Mock retry logic
    return BaseResponse(data=PayoutRetryData(retried=True))
