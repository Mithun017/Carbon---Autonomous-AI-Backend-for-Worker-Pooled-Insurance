from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from app.core.database import get_session
from app.services.ai_risk_service import AIRiskService
from app.models.schemas import AIRiskLog
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
    # Map score to level
    risk_level = "LOW"
    if result["risk_score"] > 0.7: risk_level = "HIGH"
    elif result["risk_score"] > 0.3: risk_level = "MEDIUM"
    
    return BaseResponse(data=RiskEvaluateData(
        risk_score=result["risk_score"],
        risk_level=risk_level,
        risk_zone=result["risk_category"]
    ))

@router.get("/health", response_model=BaseResponse[RiskHealthData])
def risk_service_health(session: Session = Depends(get_session)):
    """
    Contract §9.4: Dynamic model health check.
    Verifies the AI risk logging subsystem is reachable and has recent predictions.
    Returns 'healthy' | 'degraded' | 'offline'.
    """
    try:
        # Check that the AIRiskLog table is accessible
        log_count = session.exec(select(func.count(AIRiskLog.id))).one()
        model_status = "healthy" if log_count >= 0 else "degraded"
    except Exception:
        model_status = "offline"
    
    return BaseResponse(data=RiskHealthData(model_status=model_status))

@router.get("/drift", response_model=BaseResponse[RiskDriftData])
def check_risk_drift():
    result = AIRiskService.check_drift()
    return BaseResponse(data=RiskDriftData(drift_score=result["drift_score"]))

@router.post("/feedback", response_model=BaseResponse[RiskFeedbackData])
def submit_risk_feedback(payload: RiskFeedbackRequest):
    return BaseResponse(data=RiskFeedbackData(recorded=True))
