from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, workers, policy, pool, claims, trigger, 
    pricing, fraud, risk, payout, notify, analytics, ledger
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(workers.router, prefix="/workers", tags=["workers"])
api_router.include_router(policy.router, prefix="/policy", tags=["policy"])
api_router.include_router(pool.router, prefix="/pool", tags=["pool"])
api_router.include_router(claims.router, prefix="/claims", tags=["claims"])
api_router.include_router(trigger.router, prefix="/trigger", tags=["trigger"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
api_router.include_router(fraud.router, prefix="/fraud", tags=["fraud"])
api_router.include_router(risk.router, prefix="/risk", tags=["risk"])
api_router.include_router(payout.router, prefix="/payout", tags=["payout"])
api_router.include_router(notify.router, prefix="/notify", tags=["notify"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(ledger.router, prefix="/ledger", tags=["ledger"])
