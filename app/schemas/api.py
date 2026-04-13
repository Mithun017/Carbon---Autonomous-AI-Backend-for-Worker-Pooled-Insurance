from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# Auth
class OTPRequest(BaseModel):
    phone: str

class OTPVerify(BaseModel):
    phone: str
    otp: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    token_type: str = "bearer"

# Worker
class WorkerBase(BaseModel):
    phone: str
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class WorkerCreate(WorkerBase):
    pass

class WorkerRead(WorkerBase):
    id: UUID
    is_active: bool
    is_verified: bool
    balance: float
    created_at: datetime

# Policy
class PolicyOptIn(BaseModel):
    worker_id: UUID
    premium_amount: float

class PolicyRead(BaseModel):
    id: UUID
    worker_id: UUID
    is_opted_in: bool
    premium_amount: float
    last_payment_date: Optional[datetime]

# Pool & Ledger
class PoolStatus(BaseModel):
    total_balance: float
    last_audit_date: datetime

class LedgerRead(BaseModel):
    id: UUID
    transaction_type: str
    amount: float
    description: str
    created_at: datetime

# Claims
class ClaimCreate(BaseModel):
    worker_id: UUID
    event_type: str # WEATHER, PLATFORM, SOCIAL
    amount: float

class ClaimRead(BaseModel):
    id: UUID
    worker_id: UUID
    event_type: str
    status: str
    amount: float
    fraud_score: float
    decision_reason: Optional[str]
    created_at: datetime
