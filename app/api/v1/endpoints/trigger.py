from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.schemas import Policy
from app.services.claims import ClaimService
from app.services.trigger_service import TriggerService
from app.schemas.api import (
    BaseResponse, TriggerMockRequest, TriggerMockData,
    TriggerWeatherRequest, TriggerWeatherData, TriggerActiveData,
    TriggerStopRequest, TriggerStopData
)
from typing import List, Any
import random
import uuid

router = APIRouter()

@router.post("/mock", response_model=BaseResponse[TriggerMockData])
async def mock_disruption(payload: TriggerMockRequest, session: Session = Depends(get_session)):
    """
    Simulates a weather or platform disaster.
    """
    event_id = f"evt_{uuid.uuid4().hex[:8]}"
    
    # Trigger the full autonomous cycle
    from app.services.orchestration_service import OrchestrationEngine
    event_data = {"type": payload.event_type, "id": event_id}
    await OrchestrationEngine.run_automation_cycle(session, event_data)
            
    return BaseResponse(data=TriggerMockData(
        event_id=event_id,
        triggered=True
    ))

@router.post("/weather", response_model=BaseResponse[TriggerWeatherData])
def trigger_weather(payload: TriggerWeatherRequest):
    return BaseResponse(data=TriggerWeatherData(event_detected=True))

@router.get("/active", response_model=BaseResponse[TriggerActiveData])
def get_active_disruptions():
    events = TriggerService.get_active_disruptions()
    return BaseResponse(data=TriggerActiveData(events=events if isinstance(events, list) else []))

@router.post("/stop", response_model=BaseResponse[TriggerStopData])
def stop_simulation(payload: TriggerStopRequest):
    return BaseResponse(data=TriggerStopData(stopped=True))
