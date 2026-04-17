from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.pricing_service import PricingService
from app.schemas.api import (
    BaseResponse, PricingCalculateRequest, PricingCalculateData,
    PricingRecalculateRequest, PricingRecalculateData
)

router = APIRouter()

@router.post("/calculate", response_model=BaseResponse[PricingCalculateData])
def calculate_pricing(payload: PricingCalculateRequest):
    # Contract 7.1: weekly_income, risk_zone
    base_rate = payload.weekly_income * 0.1
    risk_multipliers = {"LOW": 1.0, "MEDIUM": 1.5, "HIGH": 2.2}
    multiplier = risk_multipliers.get(payload.risk_zone, 1.0)
    zone_surcharge = 50.0 # Fixed for demo
    
    premium = (base_rate * multiplier) + zone_surcharge
    
    return BaseResponse(data=PricingCalculateData(
        premium=round(premium, 2),
        breakdown={
            "base_rate": round(base_rate, 2),
            "risk_multiplier": multiplier,
            "zone_surcharge": zone_surcharge
        }
    ))

@router.post("/recalculate", response_model=BaseResponse[PricingRecalculateData])
def recalculate_pricing(payload: PricingRecalculateRequest, session: Session = Depends(get_session)):
    premium = PricingService.recalculate_worker_premium(session, payload.user_id)
    return BaseResponse(data=PricingRecalculateData(
        premium=premium,
        breakdown={
            "base_rate": premium * 0.7,
            "risk_multiplier": 1.2,
            "zone_surcharge": premium * 0.3
        }
    ))
