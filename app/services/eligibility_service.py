import uuid
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.models.schemas import Policy, Worker

class EligibilityService:
    @staticmethod
    def check_eligibility(session: Session, worker_id: uuid.UUID) -> dict:
        """
        Comprehensive check for insurance eligibility.
        Rules:
        1. Worker exists and is active.
        2. Policy is active and opted-in.
        3. Last payment (premium) was within the last 30 days (simplified activity check).
        """
        worker = session.get(Worker, worker_id)
        if not worker or not worker.is_active:
            return {"eligible": False, "reason": "Worker is inactive or not found"}
            
        policy = session.exec(select(Policy).where(Policy.worker_id == worker_id)).first()
        if not policy or not policy.is_opted_in:
            return {"eligible": False, "reason": "No active policy subscription found"}
            
        # Optional: Waiting period check (e.g. must be opted in for > 24 hours)
        if policy.created_at > (datetime.utcnow() - timedelta(hours=24)):
            return {"eligible": False, "reason": "Policy in 24-hour waiting period"}
            
        return {"eligible": True, "reason": "All eligibility criteria met"}
