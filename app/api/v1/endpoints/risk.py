from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.ai_risk_service import AIRiskService
from app.schemas.api import (
    BaseResponse, RiskEvaluateRequest, RiskEvaluateData,
    RiskDriftData, RiskFeedbackRequest, RiskFeedbackData,
    RiskHealthData
)
from typing import Any
import uuid

router = APIRouter()

@router.post("/evaluate", response_model=BaseResponse[RiskEvaluateData])
def evaluate_risk(payload: RiskEvaluateRequest, session: Session = Depends(get_session)):
    # Contract: user_id, location, activity_data
    result = AIRiskService.evaluate_risk(uuid.UUID(payload.user_id), session)
    return BaseResponse(data=RiskEvaluateData(
        risk_score=result["risk_score"],
        risk_zone=result["risk_category"] # Map category to zone for now
    ))

@router.get("/drift", response_model=BaseResponse[RiskDriftData])
def check_risk_drift():
    result = AIRiskService.check_drift()
    return BaseResponse(data=RiskDriftData(drift_score=result["drift_score"]))

@router.post("/feedback", response_model=BaseResponse[RiskFeedbackData])
def submit_risk_feedback(payload: RiskFeedbackRequest):
    return BaseResponse(data=RiskFeedbackData(recorded=True))

@router.get("/health", response_model=BaseResponse[RiskHealthData])
def risk_service_health():
    return BaseResponse(data=RiskHealthData(model_status="healthy"))
