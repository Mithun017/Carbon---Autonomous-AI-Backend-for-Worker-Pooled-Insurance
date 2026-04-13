import random
from sqlmodel import Session
from app.models.schemas import Claim, Payout, Worker
from app.services.pool import PoolService
import uuid

class FraudService:
    @staticmethod
    def evaluate_claim(claim_amount: float, worker_id: uuid.UUID):
        # MOCK AI Logic: Random score between 0 and 1
        # In production, this would call a ML model or Gemini API
        score = random.random()
        return score

class ClaimService:
    @staticmethod
    def process_auto_claim(session: Session, worker_id: uuid.UUID, event_type: str, amount: float):
        # 1. Check if fraud
        fraud_score = FraudService.evaluate_claim(amount, worker_id)
        
        status = "APPROVED"
        reason = "Auto-approved by AI risk model"
        
        if fraud_score > 0.8:
            status = "FRAUD_DETECTED"
            reason = "High fraud risk score detected"
        elif amount > 5000: # Threshold example
            status = "PENDING"
            reason = "Amount exceeds auto-approval threshold"

        claim = Claim(
            worker_id=worker_id,
            event_type=event_type,
            amount=amount,
            status=status,
            fraud_score=fraud_score,
            decision_reason=reason
        )
        session.add(claim)
        session.commit()
        session.refresh(claim)
        
        # 2. If approved, trigger payout
        if status == "APPROVED":
            ClaimService.trigger_payout(session, claim)
            
        return claim

    @staticmethod
    def trigger_payout(session: Session, claim: Claim):
        # IDEMPOTENCY CHECK
        idempotency_key = f"claim_{claim.id}"
        
        # Check if payout already exists
        # (Simplified: in production, check DB for idempotency_key)
        
        try:
            # 1. Withdraw from Pool
            PoolService.withdraw(
                session, 
                claim.amount, 
                f"Payout for claim {claim.id}", 
                worker_id=claim.worker_id,
                reference_id=str(claim.id)
            )
            
            # 2. Record Payout
            payout = Payout(
                claim_id=claim.id,
                worker_id=claim.worker_id,
                amount=claim.amount,
                status="PROCESSED",
                idempotency_key=idempotency_key
            )
            session.add(payout)
            session.commit()
            
            # 3. Notify Worker (Service call here)
            print(f"DEBUG: Payout of {claim.amount} sent to worker {claim.worker_id}")
            
        except Exception as e:
            print(f"ERROR: Payout failed: {str(e)}")
            session.rollback()
            # Mark claim as failed or retry-needed
