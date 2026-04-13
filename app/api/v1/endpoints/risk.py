from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.ai_risk_service import AIRiskService
import uuid

router = APIRouter()

@router.post("/evaluate")
def evaluate_risk(worker_id: uuid.UUID, session: Session = Depends(get_session)):
    return AIRiskService.evaluate_risk(worker_id, session)

@router.get("/health")
def risk_service_health():
    return {"status": "HEALTHY", "model_version": "v1.0.4"}

@router.get("/drift")
def check_risk_drift():
    return AIRiskService.check_drift()

@router.post("/feedback")
def submit_risk_feedback(prediction_id: str, is_accurate: bool):
    return {"message": "Feedback recorded", "prediction_id": prediction_id}
