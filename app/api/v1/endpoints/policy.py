from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.schemas.api import (
    BaseResponse, PolicyCreateRequest, PolicyCreateData,
    PolicyData, PolicyValidateRequest, PolicyValidateData,
    PolicyCancelData
)
from app.models.schemas import Policy, Worker
from app.services.pool import PoolService
from uuid import UUID
from datetime import datetime

router = APIRouter()

@router.post("/create", response_model=BaseResponse[PolicyCreateData])
def create_policy(payload: PolicyCreateRequest, session: Session = Depends(get_session)):
    worker = session.get(Worker, UUID(payload.user_id))
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    policy = session.exec(select(Policy).where(Policy.worker_id == UUID(payload.user_id))).first()
    if not policy:
        policy = Policy(worker_id=UUID(payload.user_id))
        
    policy.is_opted_in = True
    policy.premium_amount = payload.premium
    policy.last_payment_date = datetime.utcnow()
    
    session.add(policy)
    
    # Contribute to pool
    PoolService.contribute(session, UUID(payload.user_id), payload.premium)
    
    session.commit()
    session.refresh(policy)
    
    return BaseResponse(data=PolicyCreateData(
        policy_id=str(policy.id),
        active=True
    ))

@router.get("/{user_id}", response_model=BaseResponse[PolicyData])
def get_policy(user_id: UUID, session: Session = Depends(get_session)):
    policy = session.exec(select(Policy).where(Policy.worker_id == user_id)).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
        
    return BaseResponse(data=PolicyData(
        policy_id=str(policy.id),
        premium=policy.premium_amount,
        status="active" if policy.is_opted_in else "inactive"
    ))

@router.post("/validate", response_model=BaseResponse[PolicyValidateData])
def validate_policy(payload: PolicyValidateRequest, session: Session = Depends(get_session)):
    policy = session.exec(select(Policy).where(Policy.worker_id == UUID(payload.user_id))).first()
    is_valid = policy is not None and policy.is_opted_in
    return BaseResponse(data=PolicyValidateData(is_valid=is_valid))

@router.post("/cancel/{user_id}", response_model=BaseResponse[PolicyCancelData])
def cancel_policy(user_id: UUID, session: Session = Depends(get_session)):
    policy = session.exec(select(Policy).where(Policy.worker_id == user_id)).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
        
    policy.is_opted_in = False
    session.add(policy)
    session.commit()
    
    return BaseResponse(data=PolicyCancelData(cancelled=True))
