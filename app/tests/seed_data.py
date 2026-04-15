import uuid
import random
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.core.database import engine, init_db
from app.models.schemas import Worker, Policy, Pool, Claim, Ledger, Notification

def seed_database():
    print("[SEEDER] Initializing database...")
    from app.models import schemas # Ensure all tables registered
    init_db()
    
    with Session(engine) as session:
        # 1. Create Pool if not exists
        pool = session.exec(select(Pool)).first()
        if not pool:
            pool = Pool(total_balance=100000.0, reserve_threshold=20000.0)
            session.add(pool)
            session.commit()
            print("[SEEDER] Created resource pool.")

        # 2. Create 100 Workers
        print("[SEEDER] Creating 100 workers and policies...")
        zones = ["MR-1", "MR-2", "DR-1", "DR-2", "ZONE-A", "ZONE-B"]
        names = ["Aarav", "Aditi", "Arjun", "Ananya", "Ishaan", "Kavya", "Mohal", "Priya", "Rahul", "Saanvi"]
        
        for i in range(100):
            worker_id = uuid.uuid4()
            worker = Worker(
                id=worker_id,
                phone=f"99000{i:05d}",
                email=f"worker{i}@carbon.ai",
                full_name=f"{random.choice(names)} {i}",
                zone=random.choice(zones),
                weekly_income=random.uniform(300, 1200),
                is_active=True
            )
            session.add(worker)
            
            # Create Policy for each worker
            policy = Policy(
                worker_id=worker_id,
                is_opted_in=True,
                premium_amount=250.0,
                last_payment_date=datetime.utcnow() - timedelta(days=random.randint(1, 10)),
                coverage_limit=5000.0
            )
            session.add(policy)
            
        session.commit()
        print(f"[SEEDER] Successfully seeded 100 workers.")

        # 3. Create some history (Claims & Payouts)
        print("[SEEDER] Simulating claim history...")
        workers = session.exec(select(Worker)).all()
        for i in range(20):
            worker = random.choice(workers)
            claim = Claim(
                worker_id=worker.id,
                event_type=random.choice(["RAIN", "APP_CRASH", "HEATWAVE"]),
                amount=500.0,
                status="APPROVED",
                fraud_score=random.uniform(0.0, 0.2),
                ai_risk_score=random.uniform(0.1, 0.4),
                decision_reason="Historical seed data"
            )
            session.add(claim)
            
            # Ledger entry
            ledger = Ledger(
                worker_id=worker.id,
                amount=-500.0,
                transaction_type="PAYOUT",
                status="COMPLETED",
                reference_id=f"seed_tx_{i}"
            )
            session.add(ledger)
            
            # Notification
            notif = Notification(
                worker_id=worker.id,
                title="Payout Processed",
                message="Your disruption claim was approved and paid.",
                type="PAYOUT",
                status="SENT"
            )
            session.add(notif)
            
        session.commit()
        print("[SEEDER] Simulation complete.")

if __name__ == "__main__":
    seed_database()
