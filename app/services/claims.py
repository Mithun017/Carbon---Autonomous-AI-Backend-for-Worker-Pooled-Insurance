from sqlmodel import Session
from app.models.schemas import Claim, Worker, Policy
from app.services.fraud_service import FraudService
from app.services.ai_risk_service import AIRiskService
from app.services.payout_service import PayoutService
from app.services.notification_service import NotificationService
import uuid

class ClaimService:
    @staticmethod
    def process_auto_claim(session: Session, worker_id: uuid.UUID, event_type: str, amount: float):
        # 1. Check Policy Eligibility
        from sqlmodel import select
        policy = session.exec(select(Policy).where(Policy.worker_id == worker_id)).first()
        if not policy or not policy.is_opted_in:
            return None # Not eligible
            
        # 2. Evaluate AI Risk
        risk_result = AIRiskService.evaluate_risk(worker_id, session)
        risk_score = risk_result["risk_score"]
        
        # 3. Evaluate Fraud Risk
        fraud_result = FraudService.run_check(worker_id, amount)
        fraud_score = fraud_result["fraud_score"]
        
        # 4. Determine Status
        status = "APPROVED"
        reason = "Auto-approved by Carbon AI Engine"
        
        if fraud_result["is_fraud"]:
            status = "FRAUD_DETECTED"
            reason = "High fraud risk score"
        elif risk_score > 0.8:
            status = "PENDING"
            reason = "High risk evaluation - manual review required"
        elif amount > 5000:
            status = "PENDING"
            reason = "Amount exceeds auto-threshold"

        # 5. Create Claim Record
        claim = Claim(
            worker_id=worker_id,
            event_type=event_type,
            amount=amount,
            status=status,
            fraud_score=fraud_score,
            ai_risk_score=risk_score,
            decision_reason=reason
        )
        session.add(claim)
        session.commit()
        session.refresh(claim)
        
        # 6. Trigger Notification about claim initiation
        NotificationService.send_notification(
            session, 
            worker_id, 
            "Claim Initiated", 
            f"Your {event_type} claim for ${amount} is being processed. Status: {status}",
            "CLAIM"
        )
        
        # 7. If approved, process payout
        if status == "APPROVED":
            PayoutService.process_payout(session, claim.id, worker_id, amount)
            
        return claim
