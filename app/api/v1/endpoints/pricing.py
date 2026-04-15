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
    # Contract: user_id, weekly_income, risk_zone
    # For now, we use a simple calculation logic
    premium = PricingService.calculate_premium(payload.weekly_income * 0.05, 0.5)
    return BaseResponse(data=PricingCalculateData(
        premium=premium,
        breakdown={"base": premium * 0.8, "tax": premium * 0.2}
    ))

@router.post("/recalculate", response_model=BaseResponse[PricingRecalculateData])
def recalculate_pricing(payload: PricingRecalculateRequest, session: Session = Depends(get_session)):
    premium = PricingService.recalculate_worker_premium(session, payload.user_id)
    return BaseResponse(data=PricingRecalculateData(updated_premium=premium))
