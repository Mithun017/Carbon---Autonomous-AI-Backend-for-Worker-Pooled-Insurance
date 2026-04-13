from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.schemas.api import PoolStatus, LedgerRead
from app.models.schemas import Pool, Ledger
from app.services.pool import PoolService
from typing import List
from uuid import UUID

router = APIRouter()

@router.get("/status", response_model=PoolStatus)
def get_pool_status(session: Session = Depends(get_session)):
    pool = PoolService.get_pool(session)
    return pool

@router.get("/ledger/{user_id}", response_model=List[LedgerRead])
def get_user_ledger(user_id: UUID, session: Session = Depends(get_session)):
    entries = session.exec(select(Ledger).where(Ledger.worker_id == user_id)).all()
    return entries
