from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.schemas.api import (
    BaseResponse, WorkerProfileRequest, WorkerProfileData, 
    WorkerData, WorkerStatusData
)
from app.models.schemas import Worker
from uuid import UUID

router = APIRouter()

@router.post("/profile", response_model=BaseResponse[WorkerProfileData])
def create_profile(payload: WorkerProfileRequest, session: Session = Depends(get_session)):
    # Contract: user_id, name, phone, zone
    worker = session.get(Worker, UUID(payload.user_id))
    if not worker:
        # If not found by ID (UUID), try finding by phone or create new
        worker = session.exec(select(Worker).where(Worker.phone == payload.phone)).first()
        if not worker:
            worker = Worker(id=UUID(payload.user_id), phone=payload.phone)
            session.add(worker)
    
    worker.full_name = payload.name
    worker.zone = payload.zone
    session.add(worker)
    session.commit()
    
    return BaseResponse(data=WorkerProfileData(profile_created=True))

@router.get("/{id}", response_model=BaseResponse[WorkerData])
def get_worker(id: UUID, session: Session = Depends(get_session)):
    worker = session.get(Worker, id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    return BaseResponse(data=WorkerData(
        user_id=str(worker.id),
        name=worker.full_name or "Unknown",
        zone=worker.zone or "GENERAL",
        weekly_income=worker.weekly_income or 0.0
    ))

@router.get("/status/{id}", response_model=BaseResponse[WorkerStatusData])
def get_worker_status(id: UUID, session: Session = Depends(get_session)):
    worker = session.get(Worker, id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Mock eligibility logic
    return BaseResponse(data=WorkerStatusData(
        is_active=worker.is_active,
        eligible_for_claim=True
    ))
