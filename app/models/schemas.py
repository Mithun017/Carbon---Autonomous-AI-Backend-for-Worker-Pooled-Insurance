from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
import uuid

class TimestampModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Worker(TimestampModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    phone: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    balance: float = Field(default=0.0)

class Policy(TimestampModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    worker_id: uuid.UUID = Field(foreign_key="worker.id")
    is_opted_in: bool = Field(default=False)
    premium_amount: float = Field(default=0.0)
    last_payment_date: Optional[datetime] = None

class Pool(TimestampModel, table=True):
    id: int = Field(default=1, primary_key=True)
    total_balance: float = Field(default=0.0)
    last_audit_date: datetime = Field(default_factory=datetime.utcnow)

class Ledger(TimestampModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    transaction_type: str  # PREMIUM, PAYOUT, CONTRIBUTION, WITHDRAW
    amount: float
    worker_id: Optional[uuid.UUID] = Field(default=None, foreign_key="worker.id")
    description: str
    reference_id: Optional[str] = None  # To link to Claims or Payouts

class Claim(TimestampModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    worker_id: uuid.UUID = Field(foreign_key="worker.id")
    event_type: str # WEATHER, PLATFORM, SOCIAL
    status: str = Field(default="PENDING") # PENDING, APPROVED, REJECTED, FRAUD_DETECTED
    amount: float
    fraud_score: float = Field(default=0.0)
    ai_risk_score: float = Field(default=0.0)
    decision_reason: Optional[str] = None

class AIRiskLog(TimestampModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    worker_id: uuid.UUID = Field(foreign_key="worker.id")
    prediction_id: str = Field(index=True)
    risk_score: float
    risk_category: str # LOW, MEDIUM, HIGH
    premium_multiplier: float
    confidence: float
    top_factors: str # JSON string of factors

class Notification(TimestampModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    worker_id: uuid.UUID = Field(foreign_key="worker.id")
    title: str
    message: str
    type: str # DISRUPTION, CLAIM, PAYOUT, SYSTEM
    status: str = Field(default="SENT") # SENT, READ, FAILED
    retry_count: int = Field(default=0)

class Payout(TimestampModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    claim_id: uuid.UUID = Field(foreign_key="claim.id")
    worker_id: uuid.UUID = Field(foreign_key="worker.id")
    amount: float
    status: str = Field(default="PROCESSED") # PROCESSED, FAILED, RETRIED
    idempotency_key: str = Field(unique=True)
