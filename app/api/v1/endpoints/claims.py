from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.schemas import Claim
from app.services.claims import ClaimService
from app.schemas.api import (
    BaseResponse, ClaimAutoRequest, ClaimAutoData,
    ClaimData, ClaimHistoryData
)
from typing import List, Any
from uuid import UUID

router = APIRouter()

@router.post("/auto", response_model=BaseResponse[ClaimAutoData])
def trigger_auto_claim(payload: ClaimAutoRequest, session: Session = Depends(get_session)):
    # Contract: event_id, Response: claims_created
    # Since we don't have a specific 'event' mapping yet, we mock the count
    return BaseResponse(data=ClaimAutoData(claims_created=5))

@router.get("/{user_id}", response_model=BaseResponse[List[ClaimData]])
def get_user_claims(user_id: UUID, session: Session = Depends(get_session)):
    claims = session.exec(select(Claim).where(Claim.worker_id == user_id)).all()
    data = [
        ClaimData(
            claim_id=str(c.id),
            status=c.status,
            amount=c.amount
        ) for c in claims
    ]
    return BaseResponse(data=data)

@router.get("/history/{user_id}", response_model=BaseResponse[ClaimHistoryData])
def get_claim_history(user_id: UUID, session: Session = Depends(get_session)):
    claims = session.exec(select(Claim).where(Claim.worker_id == user_id)).all()
    total_amount = sum(c.amount for c in claims)
    return BaseResponse(data=ClaimHistoryData(
        total_claims=len(claims),
        total_amount=total_amount
    ))
