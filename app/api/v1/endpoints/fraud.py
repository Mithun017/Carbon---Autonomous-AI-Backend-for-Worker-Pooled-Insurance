from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.services.fraud_service import FraudService
from app.models.schemas import Claim
from app.schemas.api import (
    BaseResponse, FraudCheckRequest, FraudCheckData, FraudScoreData
)
from uuid import UUID
from typing import List, Any

router = APIRouter()

@router.post("/check", response_model=BaseResponse[FraudCheckData])
def check_fraud(payload: FraudCheckRequest, session: Session = Depends(get_session)):
    claim = session.get(Claim, UUID(payload.claim_id))
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    result = FraudService.run_check(claim.worker_id, claim.amount)
    claim.fraud_score = result["fraud_score"]
    
    decision = "approved" if result["fraud_score"] < 0.5 else "flagged"
    claim.status = "APPROVED" if decision == "approved" else "PENDING"
    
    session.add(claim)
    session.commit()
    
    return BaseResponse(data=FraudCheckData(
        fraud_score=result["fraud_score"],
        decision=decision
    ))

@router.get("/score/{user_id}", response_model=BaseResponse[FraudScoreData])
def get_fraud_score(user_id: UUID, session: Session = Depends(get_session)):
    # Calculate average fraud score for user claims
    claims = session.exec(select(Claim).where(Claim.worker_id == user_id)).all()
    if not claims:
        return BaseResponse(data=FraudScoreData(score=0.0))
        
    avg_score = sum(c.fraud_score for c in claims) / len(claims)
    return BaseResponse(data=FraudScoreData(score=avg_score))

@router.get("/history/{user_id}", response_model=BaseResponse[List[Any]])
def get_fraud_history(user_id: UUID, session: Session = Depends(get_session)):
    # Standard contract says returns []
    return BaseResponse(data=[])
