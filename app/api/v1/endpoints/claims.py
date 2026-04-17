from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.schemas import Claim, Worker, Policy
from app.services.claims import ClaimService
from app.schemas.api import (
    BaseResponse, ClaimAutoRequest, ClaimAutoData,
    ClaimData, ClaimHistoryData
)
from typing import List, Any
from uuid import UUID
from datetime import datetime

router = APIRouter()

@router.post("/auto", response_model=BaseResponse[ClaimAutoData])
def trigger_auto_claim(payload: ClaimAutoRequest, session: Session = Depends(get_session)):
    """
    Contract 5.1: Trigger auto-claims for all eligible workers for a given event_id.
    Runs the real claim pipeline (risk + fraud + payout) for opted-in workers.
    """
    # Fetch all active opted-in workers
    workers = session.exec(
        select(Worker).where(Worker.is_active == True)
    ).all()

    claims_triggered = 0
    claims_created = 0

    for worker in workers:
        # Only process eligible (opted-in) workers
        policy = session.exec(select(Policy).where(Policy.worker_id == worker.id)).first()
        if not policy or not policy.is_opted_in:
            continue

        claims_triggered += 1
        try:
            claim = ClaimService.process_auto_claim(
                session,
                worker.id,
                "GENERAL",           # generic event type for manual auto trigger
                amount=500.0,
                event_id=payload.event_id
            )
            if claim:
                claims_created += 1
        except Exception:
            continue

    return BaseResponse(data=ClaimAutoData(
        claims_triggered=claims_triggered,
        claims_created=claims_created
    ))

@router.get("/{user_id}", response_model=BaseResponse[List[ClaimData]])
def get_user_claims(user_id: UUID, session: Session = Depends(get_session)):
    # Contract 5.2: claim_id, user_id, event_id, status, amount, created_at
    claims = session.exec(select(Claim).where(Claim.worker_id == user_id).order_by(Claim.created_at.desc())).all()
    data = [
        ClaimData(
            claim_id=str(c.id),
            user_id=str(c.worker_id),
            event_id=c.event_id or "EVT-MOCK",
            status=c.status.lower(),
            amount=c.amount,
            created_at=c.created_at.isoformat() if c.created_at else datetime.utcnow().isoformat()
        ) for c in claims
    ]
    return BaseResponse(data=data)

@router.get("/history/{user_id}", response_model=BaseResponse[List[ClaimHistoryData]])
def get_claim_history(user_id: UUID, session: Session = Depends(get_session)):
    # Contract 5.3: List of historical claims
    claims = session.exec(select(Claim).where(Claim.worker_id == user_id).order_by(Claim.created_at.desc())).all()
    data = [
        ClaimHistoryData(
            claim_id=str(c.id),
            event_id=c.event_id or "EVT-MOCK",
            status=c.status.lower(),
            amount=c.amount,
            resolved_at=c.updated_at.isoformat() if c.updated_at else datetime.utcnow().isoformat()
        ) for c in claims
    ]
    return BaseResponse(data=data)
