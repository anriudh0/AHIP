from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import health, patients, claims, agents, dashboard, providers

app = FastAPI(
    title="AHIP API",
    description="AI Healthcare Intelligence Platform - Phase 0 Base",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(claims.router, prefix="/api/v1/claims", tags=["Claims"])
app.include_router(providers.router, prefix="/api/v1/providers", tags=["Providers"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
