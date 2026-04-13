from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.schemas.api import WorkerRead, WorkerCreate
from app.models.schemas import Worker
from uuid import UUID

router = APIRouter()

@router.get("/{user_id}", response_model=WorkerRead)
def get_worker(user_id: UUID, session: Session = Depends(get_session)):
    worker = session.get(Worker, user_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.post("/profile", response_model=WorkerRead)
def create_profile(payload: WorkerCreate, session: Session = Depends(get_session)):
    # Check if phone exists
    existing = session.exec(select(Worker).where(Worker.phone == payload.phone)).first()
    if existing:
        return existing
    
    worker = Worker(
        phone=payload.phone,
        full_name=payload.full_name,
        email=payload.email
    )
    session.add(worker)
    session.commit()
    session.refresh(worker)
    return worker

@router.put("/{user_id}", response_model=WorkerRead)
def update_worker(user_id: UUID, payload: WorkerCreate, session: Session = Depends(get_session)):
    worker = session.get(Worker, user_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    worker.full_name = payload.full_name
    worker.email = payload.email
    session.add(worker)
    session.commit()
    session.refresh(worker)
    return worker
