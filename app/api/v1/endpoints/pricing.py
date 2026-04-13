from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.services.pricing_service import PricingService
from pydantic import BaseModel

router = APIRouter()

class PricingRequest(BaseModel):
    base_amount: float
    risk_score: float = 0.5

@router.post("/calculate")
def calculate_pricing(payload: PricingRequest):
    premium = PricingService.calculate_premium(payload.base_amount, payload.risk_score)
    return {
        "premium_amount": premium,
        "base_amount": payload.base_amount,
        "risk_score": payload.risk_score
    }

@router.post("/recalculate")
def recalculate_pricing(worker_id: str, session: Session = Depends(get_session)):
    premium = PricingService.recalculate_worker_premium(session, worker_id)
    return {"worker_id": worker_id, "new_premium": premium}
