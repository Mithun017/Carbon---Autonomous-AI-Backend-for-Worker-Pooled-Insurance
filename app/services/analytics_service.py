from sqlmodel import Session, select, func
from app.models.schemas import Claim, Payout, Worker, Ledger, Policy
from datetime import datetime, timedelta
import random

class AnalyticsService:
    @staticmethod
    def get_dashboard_kpis(session: Session):
        """
        Aggregate high-level KPIs for the admin dashboard.
        """
        total_workers = session.exec(select(func.count(Worker.id))).one()
        total_payouts = session.exec(select(func.sum(Payout.amount))).one() or 0.0
        total_claims = session.exec(select(func.count(Claim.id))).one()
        active_policies = session.exec(select(func.count(Policy.id)).where(Policy.is_opted_in == True)).one()
        
        return {
            "total_workers": total_workers,
            "total_payout_amount": round(total_payouts, 2),
            "total_claims_count": total_claims,
            "active_policies": active_policies,
            "system_health": "OPTIMAL",
            "last_updated": datetime.utcnow().isoformat()
        }

    @staticmethod
    def get_timeseries_data(session: Session, days: int = 7):
        """
        Produce time-series data for claims and payouts.
        """
        # Simplified mock time-series
        now = datetime.utcnow()
        data = []
        for i in range(days):
            date = (now - timedelta(days=i)).date().isoformat()
            data.append({
                "date": date,
                "claims": random.randint(0, 50),
                "payouts": round(random.uniform(100, 5000), 2)
            })
        return data[::-1]
