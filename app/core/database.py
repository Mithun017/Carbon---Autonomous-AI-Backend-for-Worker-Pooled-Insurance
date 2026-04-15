from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

# Only add check_same_thread for SQLite
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL, 
    echo=settings.DEBUG,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)

def init_db():
    from app.models.schemas import Worker, Policy, Pool, Ledger, Claim, AIRiskLog, Notification, Payout, EventLog
    SQLModel.metadata.create_all(engine)

def get_session():
    with SessionLocal() as session:
        yield session
