from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Generic, TypeVar, Any
from uuid import UUID
from datetime import datetime

T = TypeVar("T")

# General Base Response
class BaseResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: Optional[str] = None
    data: Optional[T] = None

# 1. AUTH SCHEMAS
class LoginRequest(BaseModel):
    login: str = Field(..., description="phone or email")
    secret: str = Field(..., description="password or otp")

class LoginData(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str

class LogoutData(BaseModel):
    message: str = "Logged out successfully"

class OTPSendRequest(BaseModel):
    phone_number: str

class OTPSendData(BaseModel):
    otp_sent: bool

class OTPVerifyRequest(BaseModel):
    phone: str
    otp: str

class OTPVerifyData(BaseModel):
    verified: bool
    token: str

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshData(BaseModel):
    new_access_token: str

class ValidateData(BaseModel):
    is_valid: bool
    user_id: str

# 2. WORKER SCHEMAS
class WorkerProfileRequest(BaseModel):
    user_id: str
    name: str
    phone: str
    zone: str

class WorkerProfileData(BaseModel):
    profile_created: bool

class WorkerData(BaseModel):
    user_id: str
    name: str
    zone: str
    weekly_income: float

class WorkerStatusData(BaseModel):
    is_active: bool
    eligible_for_claim: bool

# 3. RISK SCHEMAS
class RiskEvaluateRequest(BaseModel):
    user_id: str
    location: str
    activity_data: Any

class RiskEvaluateData(BaseModel):
    risk_score: float
    risk_zone: str

class RiskDriftData(BaseModel):
    drift_score: float

class RiskFeedbackRequest(BaseModel):
    user_id: str
    feedback: str

class RiskFeedbackData(BaseModel):
    recorded: bool

class RiskHealthData(BaseModel):
    model_status: str

# 4. PRICING SCHEMAS
class PricingCalculateRequest(BaseModel):
    user_id: str
    weekly_income: float
    risk_zone: str

class PricingCalculateData(BaseModel):
    premium: float
    breakdown: dict

class PricingRecalculateRequest(BaseModel):
    user_id: str

class PricingRecalculateData(BaseModel):
    updated_premium: float

# 5. POLICY SCHEMAS
class PolicyCreateRequest(BaseModel):
    user_id: str
    premium: float
    plan: str

class PolicyCreateData(BaseModel):
    policy_id: str
    active: bool

class PolicyData(BaseModel):
    policy_id: str
    premium: float
    status: str

class PolicyValidateRequest(BaseModel):
    user_id: str

class PolicyValidateData(BaseModel):
    is_valid: bool

class PolicyCancelData(BaseModel):
    cancelled: bool

# 6. TRIGGER SCHEMAS
class TriggerMockRequest(BaseModel):
    event_type: str
    duration: str

class TriggerMockData(BaseModel):
    event_id: str
    triggered: bool

class TriggerWeatherRequest(BaseModel):
    location: str

class TriggerWeatherData(BaseModel):
    event_detected: bool

class TriggerActiveData(BaseModel):
    events: List[Any]

class TriggerStopRequest(BaseModel):
    event_id: str

class TriggerStopData(BaseModel):
    stopped: bool

# 7. CLAIM SCHEMAS
class ClaimAutoRequest(BaseModel):
    event_id: str

class ClaimAutoData(BaseModel):
    claims_created: int

class ClaimData(BaseModel):
    claim_id: str
    status: str
    amount: float

class ClaimHistoryData(BaseModel):
    total_claims: int
    total_amount: float

# 8. FRAUD SCHEMAS
class FraudCheckRequest(BaseModel):
    claim_id: str

class FraudCheckData(BaseModel):
    fraud_score: float
    decision: str

class FraudScoreData(BaseModel):
    score: float

# 9. PAYOUT SCHEMAS
class PayoutData(BaseModel):
    amount: float
    status: str

class PayoutProcessRequest(BaseModel):
    claim_id: str

class PayoutProcessData(BaseModel):
    payout_status: str

class PayoutRetryRequest(BaseModel):
    payout_id: str

class PayoutRetryData(BaseModel):
    retried: bool

# 10. LEDGER SCHEMAS
class LedgerEntryRequest(BaseModel):
    transaction_data: Any

class LedgerEntryData(BaseModel):
    recorded: bool

class LedgerAuditData(BaseModel):
    audit_log: List[Any]

# 11. NOTIFICATION SCHEMAS
class NotificationSendRequest(BaseModel):
    message: str
    user_id: str

class NotificationSendData(BaseModel):
    sent: bool

class NotificationRetryRequest(BaseModel):
    notification_id: str

class NotificationRetryData(BaseModel):
    retried: bool

# 12. ANALYTICS SCHEMAS
class AnalyticsDashboardData(BaseModel):
    total_workers: int
    total_payout: float

# 13. POOL SCHEMAS
class PoolStatusData(BaseModel):
    balance: float

# 14. GENERAL
class GeneralHealthData(BaseModel):
    message: str = "API Running"
