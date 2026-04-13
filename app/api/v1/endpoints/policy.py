from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.schemas.api import PolicyRead, PolicyOptIn
from app.models.schemas import Policy, Worker
from app.services.pool import PoolService
from uuid import UUID
from datetime import datetime

router = APIRouter()

@router.post("/opt-in", response_model=PolicyRead)
def opt_in(payload: PolicyOptIn, session: Session = Depends(get_session)):
    worker = session.get(Worker, payload.worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Check if already opted in
    policy = session.exec(select(Policy).where(Policy.worker_id == payload.worker_id)).first()
    if not policy:
        policy = Policy(worker_id=payload.worker_id)
        
    policy.is_opted_in = True
    policy.premium_amount = payload.premium_amount
    policy.last_payment_date = datetime.utcnow()
    
    session.add(policy)
    
    # Initial contribution
    PoolService.contribute(session, payload.worker_id, payload.premium_amount)
    
    session.commit()
    session.refresh(policy)
    return policy

@router.get("/{user_id}", response_model=PolicyRead)
def get_policy(user_id: UUID, session: Session = Depends(get_session)):
    policy = session.exec(select(Policy).where(Policy.worker_id == user_id)).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy
