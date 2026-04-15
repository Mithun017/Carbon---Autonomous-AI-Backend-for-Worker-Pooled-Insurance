from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/api/v1/openapi.json",
    debug=settings.DEBUG
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import asyncio
from app.services.orchestration_service import OrchestrationEngine

@app.on_event("startup")
def on_startup():
    init_db()
    # Start autonomous monitoring in the background
    asyncio.create_task(OrchestrationEngine.background_monitor())

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "success", "message": "API Running"}
