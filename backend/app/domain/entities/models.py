from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.session import Base

class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    plan_id: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="Active")
    risk_category: Mapped[str] = mapped_column(String(50), default="Standard")

class Provider(Base):
    __tablename__ = "providers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    provider_type: Mapped[str] = mapped_column(String(100))
    network_status: Mapped[str] = mapped_column(String(50))

class Claim(Base):
    __tablename__ = "claims"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    claim_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    patient_member_id: Mapped[str] = mapped_column(String(50), index=True)
    provider_id: Mapped[str] = mapped_column(String(50), index=True)
    service_date: Mapped[str] = mapped_column(String(20))
    claim_status: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(Float, default=0)
    cpt_codes: Mapped[list[str]] = mapped_column(JSON, default=list)
    icd_codes: Mapped[list[str]] = mapped_column(JSON, default=list)

class BenefitPlan(Base):
    __tablename__ = "benefit_plans"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    auth_required: Mapped[bool] = mapped_column(Boolean, default=False)

class ProviderContract(Base):
    __tablename__ = "provider_contracts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    contract_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    provider_id: Mapped[str] = mapped_column(String(50), index=True)
    status: Mapped[str] = mapped_column(String(50), default="Active")

class CareTask(Base):
    __tablename__ = "care_tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), index=True)
    due_date: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50), default="Open")
    owner: Mapped[str] = mapped_column(String(100))

class WorkflowEvent(Base):
    __tablename__ = "workflow_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_id: Mapped[str] = mapped_column(String(50), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    payload: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AgentExecution(Base):
    __tablename__ = "agent_executions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_id: Mapped[str] = mapped_column(String(50), index=True)
    agent_name: Mapped[str] = mapped_column(String(100), index=True)
    output: Mapped[dict] = mapped_column(JSON, default={})
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AgentMemory(Base):
    __tablename__ = "agent_memory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    case_id: Mapped[str] = mapped_column(String(50), index=True)
    agent_name: Mapped[str] = mapped_column(String(100), index=True)
    observation: Mapped[str] = mapped_column(Text)
    recommendation: Mapped[str] = mapped_column(Text)
    evidence: Mapped[dict] = mapped_column(JSON, default={})
    confidence: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
