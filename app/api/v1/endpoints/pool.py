from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.schemas import Ledger
from app.services.pool import PoolService
from app.schemas.api import (
    BaseResponse, PoolStatusData
)
from typing import List, Any
from uuid import UUID

router = APIRouter()

@router.get("/status", response_model=BaseResponse[PoolStatusData])
def get_pool_status(session: Session = Depends(get_session)):
    pool = PoolService.get_pool(session)
    return BaseResponse(data=PoolStatusData(balance=pool.total_balance))

@router.get("/ledger/{user_id}", response_model=BaseResponse[List[Any]])
def get_pool_ledger(user_id: UUID, session: Session = Depends(get_session)):
    # Contract says returns [], so we return entries list
    entries = session.exec(select(Ledger).where(Ledger.worker_id == user_id)).all()
    return BaseResponse(data=entries)
