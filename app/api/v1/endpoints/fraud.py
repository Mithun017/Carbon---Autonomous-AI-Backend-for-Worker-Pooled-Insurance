from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.services.fraud_service import FraudService
from app.models.schemas import Claim
import uuid

router = APIRouter()

@router.post("/check")
def check_fraud(claim_id: uuid.UUID, session: Session = Depends(get_session)):
    claim = session.get(Claim, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    result = FraudService.run_check(claim.worker_id, claim.amount)
    claim.fraud_score = result["fraud_score"]
    session.add(claim)
    session.commit()
    return result

@router.get("/{claim_id}")
def get_fraud_report(claim_id: uuid.UUID, session: Session = Depends(get_session)):
    claim = session.get(Claim, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return {
        "claim_id": claim.id,
        "fraud_score": claim.fraud_score,
        "status": "FLAGGED" if claim.fraud_score > 0.8 else "CLEARED"
    }

@router.post("/override")
def fraud_override(claim_id: uuid.UUID, session: Session = Depends(get_session)):
    claim = session.get(Claim, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    claim.status = "APPROVED"
    claim.decision_reason = "Manual override by fraud investigator"
    session.add(claim)
    session.commit()
    return {"message": "Fraud check overridden, claim approved"}
