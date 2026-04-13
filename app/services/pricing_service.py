from sqlmodel import Session, select
from app.models.schemas import Policy, Worker
from decimal import Decimal
import random

class PricingService:
    @staticmethod
    def calculate_premium(base_amount: float, risk_score: float = 0.5) -> float:
        """
        Calculate premium based on base amount and risk multiplier.
        Simple formula: base * (1 + risk_score)
        """
        multiplier = 1.0 + (risk_score * 0.5) # Max 1.5x multiplier
        premium = base_amount * multiplier
        return round(float(premium), 2)

    @staticmethod
    def recalculate_worker_premium(session: Session, worker_id: str) -> float:
        """
        Check historical behavior and update premium.
        """
        # Placeholder for complex logic
        base_rate = 50.0
        random_risk = random.uniform(0.1, 0.9)
        return PricingService.calculate_premium(base_rate, random_risk)
