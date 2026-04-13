from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.schemas.api import ClaimRead, ClaimCreate
from app.models.schemas import Claim, Worker
from app.services.claims import ClaimService
from typing import List
from uuid import UUID

router = APIRouter()

@router.post("/auto", response_model=ClaimRead)
def trigger_auto_claim(payload: ClaimCreate, session: Session = Depends(get_session)):
    worker = session.get(Worker, payload.worker_id)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
        
    claim = ClaimService.process_auto_claim(
        session, 
        payload.worker_id, 
        payload.event_type, 
        payload.amount
    )
    return claim

@router.get("/{user_id}", response_model=List[ClaimRead])
def get_user_claims(user_id: UUID, session: Session = Depends(get_session)):
    claims = session.exec(select(Claim).where(Claim.worker_id == user_id)).all()
    return claims
