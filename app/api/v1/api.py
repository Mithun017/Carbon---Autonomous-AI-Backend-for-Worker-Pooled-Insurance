from fastapi import APIRouter
from app.api.v1.endpoints import auth, workers, policy, pool, claims, simulation

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(workers.router, prefix="/workers", tags=["workers"])
api_router.include_router(policy.router, prefix="/policy", tags=["policy"])
api_router.include_router(pool.router, prefix="/pool", tags=["pool"])
api_router.include_router(claims.router, prefix="/claims", tags=["claims"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
