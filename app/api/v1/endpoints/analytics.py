from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats(session: Session = Depends(get_session)):
    return AnalyticsService.get_dashboard_kpis(session)

@router.get("/timeseries")
def get_timeseries(days: int = 7, session: Session = Depends(get_session)):
    return AnalyticsService.get_timeseries_data(session, days)

@router.get("/zones")
def get_zone_analytics():
    return [
        {"zone": "Downtown", "risk_level": "LOW", "active_workers": 150},
        {"zone": "Industrial", "risk_level": "MEDIUM", "active_workers": 85},
        {"zone": "Suburbs", "risk_level": "SAFE", "active_workers": 210}
    ]
