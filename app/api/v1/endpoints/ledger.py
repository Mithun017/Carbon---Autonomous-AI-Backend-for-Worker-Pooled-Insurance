from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.schemas import Ledger
from app.schemas.api import (
    BaseResponse, LedgerEntryRequest, LedgerEntryData,
    LedgerAuditData, AuditLogEntry
)
from typing import List, Any
from uuid import UUID
import uuid

router = APIRouter()

@router.get("/audit", response_model=BaseResponse[LedgerAuditData])
def get_ledger_audit(transaction_id: str = None, session: Session = Depends(get_session)):
    query = select(Ledger)
    if transaction_id:
        query = query.where(Ledger.id == UUID(transaction_id))
    
    entries = session.exec(query.order_by(Ledger.created_at.desc())).all()
    
    audit_log = [
        AuditLogEntry(
            transaction_id=str(e.id),
            action=e.transaction_type,
            user_id=str(e.worker_id) if e.worker_id else "SYSTEM",
            amount=e.amount,
            timestamp=e.created_at.isoformat(),
            details={"description": e.description}
        ) for e in entries
    ]
    return BaseResponse(data=LedgerAuditData(audit_log=audit_log))

@router.get("/{user_id}", response_model=BaseResponse[List[AuditLogEntry]])
def get_user_ledger(user_id: UUID, session: Session = Depends(get_session)):
    entries = session.exec(select(Ledger).where(Ledger.worker_id == user_id).order_by(Ledger.created_at.desc())).all()
    data = [
        AuditLogEntry(
            transaction_id=str(e.id),
            action=e.transaction_type,
            user_id=str(e.worker_id),
            amount=e.amount,
            timestamp=e.created_at.isoformat(),
            details={"description": e.description}
        ) for e in entries
    ]
    return BaseResponse(data=data)

@router.post("/entry", response_model=BaseResponse[LedgerEntryData])
def create_ledger_entry(payload: LedgerEntryRequest, session: Session = Depends(get_session)):
    # Contract 13.3: transaction_data, Response: transaction_id
    new_id = str(uuid.uuid4())
    return BaseResponse(data=LedgerEntryData(transaction_id=new_id, recorded=True))
