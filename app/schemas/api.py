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
    otp_sent: bool = True

class OTPVerifyRequest(BaseModel):
    phone: str
    otp: str

class OTPVerifyData(BaseModel):
    verified: bool
    token: str
    access_token: Optional[str] = None # Added for contract 1.4
    refresh_token: Optional[str] = None # Added for contract 1.4

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshData(BaseModel):
    new_access_token: str
    access_token: Optional[str] = None # Support both names

class ValidateData(BaseModel):
    valid: bool # Changed from is_valid per contract 1.6
    user_id: str

# 2. WORKER SCHEMAS
class WorkerProfileRequest(BaseModel):
    user_id: str
    name: str
    phone: str
    zone: str

class WorkerProfileData(BaseModel):
    profile_created: bool = True
    user_id: Optional[str] = None # Added for contract 2.1

class WorkerData(BaseModel):
    user_id: str
    name: str
    phone: Optional[str] = None
    zone: str
    weekly_income: float

class WorkerStatusData(BaseModel):
    user_id: str
    status: str # active | inactive | suspended
    last_active: Optional[str] = None
    zone: Optional[str] = None

# 3. RISK SCHEMAS
class RiskEvaluateRequest(BaseModel):
    user_id: str
    location: str
    activity_data: Any

class RiskEvaluateData(BaseModel):
    risk_score: float
    risk_level: str # LOW | MEDIUM | HIGH per contract 9.1
    risk_zone: Optional[str] = None

class RiskDriftData(BaseModel):
    drift_score: float

class RiskFeedbackRequest(BaseModel):
    user_id: str
    feedback: str

class RiskFeedbackData(BaseModel):
    recorded: bool

class RiskHealthData(BaseModel):
    model_status: str # healthy | degraded | offline

# 4. PRICING SCHEMAS
class PricingCalculateRequest(BaseModel):
    user_id: str
    weekly_income: float
    risk_zone: str

class PricingCalculateData(BaseModel):
    premium: float
    breakdown: dict # base_rate, risk_multiplier, zone_surcharge

class PricingRecalculateRequest(BaseModel):
    user_id: str

class PricingRecalculateData(BaseModel):
    updated_premium: Optional[float] = None
    premium: Optional[float] = None
    breakdown: dict

# 5. POLICY SCHEMAS
class PolicyCreateRequest(BaseModel):
    user_id: str
    premium: float
    plan: str # BASIC | STANDARD | PREMIUM

class PolicyCreateData(BaseModel):
    policy_id: str
    user_id: str
    premium: float
    plan: str
    status: str = "active"

class PolicyData(BaseModel):
    policy_id: str
    user_id: str
    premium: float
    plan: str
    status: str

class PolicyValidateRequest(BaseModel):
    user_id: str

class PolicyValidateData(BaseModel):
    valid: bool # Changed from is_valid
    reason: Optional[str] = None

class PolicyCancelData(BaseModel):
    cancelled: bool

# 6. TRIGGER SCHEMAS
class TriggerMockRequest(BaseModel):
    event_type: str
    duration: str

class TriggerMockData(BaseModel):
    event_id: str
    event_type: str
    triggered: bool = True   # Dashboard reads this to confirm the cycle fired
    active: bool = True

class TriggerWeatherRequest(BaseModel):
    location: str

class TriggerWeatherData(BaseModel):
    event_id: Optional[str] = None
    location: Optional[str] = None
    active: bool = True
    event_detected: Optional[bool] = None

class ActiveEvent(BaseModel):
    id: str
    event_type: str
    zone: str
    active: bool

class TriggerActiveData(BaseModel):
    events: List[ActiveEvent]

class TriggerStopRequest(BaseModel):
    event_id: str

class TriggerStopData(BaseModel):
    stopped: bool

# 7. CLAIM SCHEMAS
class ClaimAutoRequest(BaseModel):
    event_id: str

class ClaimAutoData(BaseModel):
    claims_triggered: int
    claims_created: Optional[int] = None

class ClaimSummaryData(BaseModel):
    """Global claim pipeline statistics for the admin dashboard."""
    total_claims: int
    pending_claims: int
    approved_claims: int
    rejected_claims: int

class ClaimData(BaseModel):
    claim_id: str
    user_id: str
    event_id: str
    status: str # pending | approved | rejected | paid
    amount: float
    created_at: str

class ClaimHistoryData(BaseModel):
    claim_id: str
    event_id: str
    status: str
    amount: float
    resolved_at: Optional[str] = None

# 8. FRAUD SCHEMAS
class FraudCheckRequest(BaseModel):
    claim_id: str

class FraudCheckData(BaseModel):
    claim_id: str
    fraud_flag: bool
    confidence: float

class FraudScoreData(BaseModel):
    user_id: str
    fraud_score: float
    risk_level: str # LOW | MEDIUM | HIGH

# 9. PAYOUT SCHEMAS
class PayoutData(BaseModel):
    payout_id: str
    claim_id: str
    amount: float
    status: str # pending | disbursed | failed
    paid_at: Optional[str] = None

class PayoutProcessRequest(BaseModel):
    claim_id: str

class PayoutProcessData(BaseModel):
    payout_id: str
    amount: float
    status: str

class PayoutRetryRequest(BaseModel):
    payout_id: str

class PayoutRetryData(BaseModel):
    retried: bool

# 10. LEDGER SCHEMAS
class LedgerEntryRequest(BaseModel):
    transaction_data: Any

class LedgerEntryData(BaseModel):
    transaction_id: str
    recorded: Optional[bool] = None

class AuditLogEntry(BaseModel):
    transaction_id: str
    action: str
    user_id: str
    amount: float
    timestamp: str
    details: Optional[dict] = None

class LedgerAuditData(BaseModel):
    audit_log: List[AuditLogEntry]

# 11. NOTIFICATION SCHEMAS
class NotificationData(BaseModel):
    notification_id: str
    message: str
    sent_at: str
    status: str # sent | failed | pending

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
    active_policies: int
    pending_claims: int
    approved_claims: int
    rejected_claims: int
    total_claims: int
    system_health: str = "OPTIMAL"           # OPTIMAL | DEGRADED | OFFLINE
    last_updated: Optional[str] = None        # ISO timestamp of last KPI computation

class AnalyticsTimeseriesEntry(BaseModel):
    date: str
    claims: int
    payouts: float

class AnalyticsZoneEntry(BaseModel):
    zone: str
    risk_level: str
    active_workers: int

# 13. POOL SCHEMAS
class PoolStatusData(BaseModel):
    balance: float

# 14. GENERAL
class GeneralHealthData(BaseModel):
    message: str = "API Running"
