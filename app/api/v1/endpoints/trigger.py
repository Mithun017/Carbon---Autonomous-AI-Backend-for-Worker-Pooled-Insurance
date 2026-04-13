from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.schemas import Worker, Policy
from app.services.claims import ClaimService
from app.services.trigger_service import TriggerService
import random

router = APIRouter()

@router.post("/mock")
def mock_disruption(event_type: str, session: Session = Depends(get_session)):
    """
    Simulates a weather or platform disaster.
    Finds all active policy holders and triggers auto-claims for them.
    """
    active_policies = session.exec(select(Policy).where(Policy.is_opted_in == True)).all()
    
    impacted_count = 0
    for policy in active_policies:
        if random.random() > 0.3:
            ClaimService.process_auto_claim(
                session,
                policy.worker_id,
                event_type,
                amount=500.0
            )
            impacted_count += 1
            
    return {
        "status": "SUCCESS",
        "event_type": event_type,
        "impacted_workers": impacted_count
    }

@router.get("/active")
def get_active_disruptions():
    return TriggerService.get_active_disruptions()

@router.post("/stop")
def stop_simulation():
    return {"message": "All simulations stopped"}
