from sqlmodel import Session, select
from app.models.schemas import Pool, Ledger, Worker
import uuid
from typing import Optional

class LedgerService:
    @staticmethod
    def record_entry(session: Session, transaction_type: str, amount: float, description: str, worker_id: Optional[uuid.UUID] = None, reference_id: Optional[str] = None):
        entry = Ledger(
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            worker_id=worker_id,
            reference_id=reference_id
        )
        session.add(entry)
        session.flush()
        return entry

class PoolService:
    @staticmethod
    def get_pool(session: Session):
        pool = session.exec(select(Pool).where(Pool.id == 1)).first()
        if not pool:
            pool = Pool(id=1, total_balance=0.0)
            session.add(pool)
            session.commit()
            session.refresh(pool)
        return pool

    @staticmethod
    def contribute(session: Session, worker_id: uuid.UUID, amount: float):
        pool = PoolService.get_pool(session)
        worker = session.get(Worker, worker_id)
        
        if not worker:
            raise Exception("Worker not found")
            
        # Update Pool
        pool.total_balance += amount
        session.add(pool)
        
        # Record in Ledger
        LedgerService.record_entry(
            session, 
            "CONTRIBUTION", 
            amount, 
            f"Contribution from worker {worker.phone}", 
            worker_id=worker_id
        )
        
        session.commit()
        return pool

    @staticmethod
    def withdraw(session: Session, amount: float, description: str, worker_id: Optional[uuid.UUID] = None, reference_id: Optional[str] = None):
        pool = PoolService.get_pool(session)
        
        if pool.total_balance < amount:
            raise Exception("Insufficient pool balance")
            
        pool.total_balance -= amount
        session.add(pool)
        
        LedgerService.record_entry(
            session, 
            "WITHDRAW", 
            -amount, 
            description, 
            worker_id=worker_id,
            reference_id=reference_id
        )
        
        session.commit()
        return pool
