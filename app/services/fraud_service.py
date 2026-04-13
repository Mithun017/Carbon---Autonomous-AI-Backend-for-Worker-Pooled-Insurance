import random
import uuid
from datetime import datetime
from sqlmodel import Session
from app.core.config import settings

class FraudService:
    @staticmethod
    def calculate_fraud_score(worker_id: uuid.UUID, claim_amount: float) -> float:
        """
        Calculate fraud score (0 to 1).
        In production, this would analyze claim frequency, location jitter, and amount anomalies.
        """
        # Simple simulated logic
        base_score = random.uniform(0.0, 0.3)
        
        # High amount penalty
        if claim_amount > 1000:
            base_score += 0.2
        
        # Random high risk (5% chance)
        if random.random() < 0.05:
            base_score = random.uniform(0.8, 1.0)
            
        return round(base_score, 2)

    @staticmethod
    def run_check(worker_id: uuid.UUID, claim_amount: float) -> dict:
        score = FraudService.calculate_fraud_score(worker_id, claim_amount)
        is_fraud = score > settings.FRAUD_THRESHOLD_HIGH
        
        return {
            "fraud_score": score,
            "is_fraud": is_fraud,
            "checks": [
                {"name": "frequency_check", "passed": True},
                {"name": "amount_anomaly", "passed": claim_amount < 2000},
                {"name": "identity_consistency", "passed": True}
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
