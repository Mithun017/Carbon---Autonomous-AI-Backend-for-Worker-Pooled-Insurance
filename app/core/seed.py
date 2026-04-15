import uuid
import random
from sqlmodel import Session, select
from app.core.database import engine, init_db, SessionLocal
from app.models.schemas import Worker, Policy, Pool

def seed_data():
    """
    Seeds the database with 50 workers and policies to demonstrate automation.
    """
    init_db()
    with SessionLocal() as session:
        # 1. Initialize Pool
        pool = session.exec(select(Pool).where(Pool.id == 1)).first()
        if not pool:
            pool = Pool(id=1, total_balance=1000000.0) # $1M Seed Pool
            session.add(pool)
            print("Seed: Initialized Pool with $1,000,000")
            
        # 2. Check if already seeded
        existing_workers = session.exec(select(Worker)).all()
        if len(existing_workers) >= 50:
            print(f"Seed: Database already has {len(existing_workers)} workers.")
            return

        zones = ["Downtown", "Industrial", "Residential", "Suburbs"]
        names = ["Aarav", "Vihaan", "Aditya", "Sai", "Ishaan", "Arjun", "Ananya", "Diya", "Pari", "Saanvi"]
        
        print("Seed: Generating 50 workers...")
        for i in range(50):
            uid = uuid.uuid4()
            worker = Worker(
                id=uid,
                phone=f"+91{random.randint(7000000000, 9999999999)}",
                full_name=f"{random.choice(names)} {chr(65+i%26)}",
                email=f"worker_{i}@carbon.ai",
                is_active=True,
                is_verified=True,
                balance=0.0,
                zone=random.choice(zones),
                weekly_income=random.uniform(5000, 15000)
            )
            session.add(worker)
            session.flush() # Ensure worker is in DB before policy
            
            # Create Policy for each worker
            policy = Policy(
                worker_id=uid,
                is_opted_in=True,
                premium_amount=random.choice([199.0, 249.0, 299.0, 399.0]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 10))
            )
            session.add(policy)
            
        session.commit()
        print("Seed: Successfully seeded 50 workers and policies.")

if __name__ == "__main__":
    from datetime import datetime, timedelta
    seed_data()
else:
    from datetime import datetime, timedelta
