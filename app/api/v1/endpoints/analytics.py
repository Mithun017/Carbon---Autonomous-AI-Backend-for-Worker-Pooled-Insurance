from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.services.analytics_service import AnalyticsService
from app.schemas.api import (
    BaseResponse, AnalyticsDashboardData, AnalyticsZoneEntry
)
from typing import List, Any

router = APIRouter()

@router.get("/dashboard", response_model=BaseResponse[AnalyticsDashboardData])
def get_dashboard_stats(session: Session = Depends(get_session)):
    """
    Contract §12: Returns full 9-field KPI dashboard.
    """
    stats = AnalyticsService.get_dashboard_kpis(session)
    return BaseResponse(data=AnalyticsDashboardData(
        total_workers=stats.get("total_workers", 0),
        total_payout=stats.get("total_payout", 0.0),
        active_policies=stats.get("active_policies", 0),
        pending_claims=stats.get("pending_claims", 0),
        approved_claims=stats.get("approved_claims", 0),
        rejected_claims=stats.get("rejected_claims", 0),
        total_claims=stats.get("total_claims", 0),
        system_health=stats.get("system_health", "OPTIMAL"),
        last_updated=stats.get("last_updated")
    ))

@router.get("/timeseries", response_model=BaseResponse[List[Any]])
def get_timeseries(days: int = 7, session: Session = Depends(get_session)):
    data = AnalyticsService.get_timeseries_data(session, days)
    return BaseResponse(data=data if isinstance(data, list) else [])

@router.get("/zones", response_model=BaseResponse[List[AnalyticsZoneEntry]])
def get_zone_analytics(session: Session = Depends(get_session)):
    """
    Contract §12.3: Returns zone breakdown derived from Worker.zone field in the database.
    Falls back to static defaults if no workers are found.
    """
    zones = AnalyticsService.get_zone_analytics(session)
    return BaseResponse(data=zones)
