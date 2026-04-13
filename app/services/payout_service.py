import uuid
from sqlmodel import Session, select
from app.models.schemas import Payout, Worker
from app.services.pool import PoolService
from app.services.notification_service import NotificationService

class PayoutService:
    @staticmethod
    def process_payout(session: Session, claim_id: uuid.UUID, worker_id: uuid.UUID, amount: float) -> Payout:
        """
        Execute payout with idempotency and ledger tracking.
        """
        idempotency_key = f"PAY-{claim_id}"
        
        # 1. Check if already processed
        existing = session.exec(select(Payout).where(Payout.idempotency_key == idempotency_key)).first()
        if existing:
            return existing
            
        try:
            # 2. Debit Pool and Ledger Entry
            PoolService.withdraw(
                session,
                amount,
                f"Insurance Payout for Claim {claim_id}",
                worker_id=worker_id,
                reference_id=str(claim_id)
            )
            
            # 3. Create Payout Record
            payout = Payout(
                claim_id=claim_id,
                worker_id=worker_id,
                amount=amount,
                status="PROCESSED",
                idempotency_key=idempotency_key
            )
            session.add(payout)
            session.commit()
            session.refresh(payout)
            
            # 4. Trigger Notification (Async in real world, sync here for now or background task)
            NotificationService.send_notification(
                session,
                worker_id,
                "Payout Successful",
                f"A payout of ${amount} has been processed for your claim.",
                "PAYOUT"
            )
            
            return payout
            
        except Exception as e:
            session.rollback()
            # Record failed payout attempt
            print(f"PAYOUT ERROR: {str(e)}")
            raise e

    @staticmethod
    def get_user_payouts(session: Session, worker_id: uuid.UUID):
        return session.exec(select(Payout).where(Payout.worker_id == worker_id)).all()
