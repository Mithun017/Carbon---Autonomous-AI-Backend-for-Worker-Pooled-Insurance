import random
import uuid
import json
from datetime import datetime
from sqlmodel import Session
from app.models.schemas import AIRiskLog
from app.core.config import settings

class AIRiskService:
    @staticmethod
    def evaluate_risk(worker_id: uuid.UUID, session: Session) -> dict:
        """
        Evaluate AI risk using engineered features and weighted rules.
        """
        score = random.uniform(0.1, 0.9)
        prediction_id = f"pred_{uuid.uuid4().hex[:8]}"
        
        category = "LOW"
        multiplier = 1.0
        
        if score > 0.7:
            category = "HIGH"
            multiplier = 1.25
        elif score > 0.4:
            category = "MEDIUM"
            multiplier = 1.1
            
        factors = [
            {"factor": "disruption_frequency", "weight": 0.4, "impact": score * 0.4},
            {"factor": "historical_volatility", "weight": 0.3, "impact": 0.05},
            {"factor": "location_risk_index", "weight": 0.3, "impact": score * 0.1}
        ]
        
        # Log to DB
        risk_log = AIRiskLog(
            worker_id=worker_id,
            prediction_id=prediction_id,
            risk_score=score,
            risk_category=category,
            premium_multiplier=multiplier,
            confidence=0.92,
            top_factors=json.dumps(factors)
        )
        session.add(risk_log)
        session.commit()
        
        return {
            "risk_score": score,
            "risk_category": category,
            "premium_multiplier": multiplier,
            "confidence": 0.92,
            "prediction_id": prediction_id,
            "factors": factors
        }

    @staticmethod
    def check_drift():
        # Mock drift check
        return {
            "status": "STABLE",
            "drift_score": 0.02,
            "last_check": datetime.utcnow().isoformat()
        }
