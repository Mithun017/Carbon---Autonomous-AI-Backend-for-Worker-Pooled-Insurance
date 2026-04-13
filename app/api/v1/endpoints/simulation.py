from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.schemas import Worker, Policy
from app.services.claims import ClaimService
import random

router = APIRouter()

@router.post("/mock-disruption")
def mock_disruption(event_type: str, session: Session = Depends(get_session)):
    """
    Simulates a weather or platform disaster.
    Finds all active policy holders and triggers auto-claims for them.
    """
    active_policies = session.exec(select(Policy).where(Policy.is_opted_in == True)).all()
    
    impacted_count = 0
    for policy in active_policies:
        # Simulate local impact (not everyone gets hit)
        if random.random() > 0.3:
            ClaimService.process_auto_claim(
                session,
                policy.worker_id,
                event_type,
                amount=500.0 # Standard payout for mock
            )
            impacted_count += 1
            
    return {
        "status": "Disruption simulation completed",
        "event_type": event_type,
        "active_policies_at_time": len(active_policies),
        "impacted_workers": impacted_count
    }
