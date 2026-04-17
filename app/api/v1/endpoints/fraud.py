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
        claim_id=payload.claim_id,
        fraud_flag=result["fraud_score"] > 0.5,
        confidence=1.0 - result["fraud_score"]
    ))

@router.get("/score/{user_id}", response_model=BaseResponse[FraudScoreData])
def get_fraud_score(user_id: UUID, session: Session = Depends(get_session)):
    # Calculate average fraud score for user claims
    claims = session.exec(select(Claim).where(Claim.worker_id == user_id)).all()
    avg_score = 0.0
    if claims:
        avg_score = sum(c.fraud_score or 0.0 for c in claims) / len(claims)
    
    risk_level = "LOW"
    if avg_score > 0.7: risk_level = "HIGH"
    elif avg_score > 0.3: risk_level = "MEDIUM"
        
    return BaseResponse(data=FraudScoreData(
        user_id=str(user_id),
        fraud_score=round(avg_score, 2),
        risk_level=risk_level
    ))

@router.get("/history/{user_id}", response_model=BaseResponse[List[Any]])
def get_fraud_history(user_id: UUID, session: Session = Depends(get_session)):
    # Standard contract says returns []
    return BaseResponse(data=[])
