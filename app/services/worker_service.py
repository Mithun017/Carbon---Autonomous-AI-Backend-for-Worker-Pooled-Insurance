from sqlmodel import Session, select
from app.models.schemas import Worker
from app.schemas.api import WorkerCreate
import uuid
from typing import Optional

class WorkerService:
    @staticmethod
    def get_worker(session: Session, worker_id: uuid.UUID) -> Optional[Worker]:
        return session.get(Worker, worker_id)

    @staticmethod
    def get_worker_by_phone(session: Session, phone: str) -> Optional[Worker]:
        return session.exec(select(Worker).where(Worker.phone == phone)).first()

    @staticmethod
    def update_profile(session: Session, worker_id: uuid.UUID, data: dict) -> Optional[Worker]:
        worker = WorkerService.get_worker(session, worker_id)
        if not worker:
            return None
        
        for key, value in data.items():
            if hasattr(worker, key) and value is not None:
                setattr(worker, key, value)
        
        session.add(worker)
        session.commit()
        session.refresh(worker)
        return worker

    @staticmethod
    def deactivate_worker(session: Session, worker_id: uuid.UUID) -> bool:
        worker = WorkerService.get_worker(session, worker_id)
        if not worker:
            return False
        worker.is_active = False
        session.add(worker)
        session.commit()
        return True
