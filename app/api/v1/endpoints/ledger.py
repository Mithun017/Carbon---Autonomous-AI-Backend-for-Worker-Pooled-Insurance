from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.schemas import Ledger
import uuid

router = APIRouter()

@router.get("/{user_id}")
def get_user_ledger(user_id: uuid.UUID, session: Session = Depends(get_session)):
    entries = session.exec(select(Ledger).where(Ledger.worker_id == user_id)).all()
    return entries

@router.post("/entry")
def create_ledger_entry(
    transaction_type: str, 
    amount: float, 
    description: str, 
    worker_id: uuid.UUID = None, 
    reference_id: str = None, 
    session: Session = Depends(get_session)
):
    entry = Ledger(
        transaction_type=transaction_type,
        amount=amount,
        description=description,
        worker_id=worker_id,
        reference_id=reference_id
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

@router.get("/audit/{transaction_id}")
def get_ledger_audit(transaction_id: uuid.UUID, session: Session = Depends(get_session)):
    entry = session.get(Ledger, transaction_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return entry
