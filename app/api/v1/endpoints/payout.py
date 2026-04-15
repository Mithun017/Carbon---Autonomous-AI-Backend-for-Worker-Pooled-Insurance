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
    payouts = PayoutService.get_user_payouts(session, user_id)
    data = [
        PayoutData(
            amount=p.amount,
            status=p.status
        ) for p in payouts
    ]
    return BaseResponse(data=data)

@router.post("/process", response_model=BaseResponse[PayoutProcessData])
def process_payout(payload: PayoutProcessRequest, session: Session = Depends(get_session)):
    # Contract: claim_id, Response: payout_status
    # We need to find the claim to get worker_id and amount
    from app.models.schemas import Claim
    claim = session.get(Claim, UUID(payload.claim_id))
    if not claim:
         raise HTTPException(status_code=404, detail="Claim not found")
         
    try:
        payout = PayoutService.process_payout(session, claim.id, claim.worker_id, claim.amount)
        return BaseResponse(data=PayoutProcessData(payout_status=payout.status))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/retry", response_model=BaseResponse[PayoutRetryData])
def retry_payout(payload: PayoutRetryRequest, session: Session = Depends(get_session)):
    # Mock retry logic
    return BaseResponse(data=PayoutRetryData(retried=True))
