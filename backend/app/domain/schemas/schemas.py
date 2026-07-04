from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class AgentRunRequest(BaseModel):
    case_id: str

class AgentOutput(BaseModel):
    agent_name: str
    case_id: str
    risk_level: str
    observation: str
    recommendation: str
    evidence: list[str]
    confidence: float
    next_owner: str | None = None

class DashboardSummary(BaseModel):
    open_cases: int
    high_risk_cases: int
    claim_exceptions: int
    provider_contract_issues: int
    compliance_gaps: int

class PatientResponse(BaseModel):
    id: int
    member_id: str
    name: str
    plan_id: str
    status: str
    risk_category: str
    model_config = ConfigDict(from_attributes=True)

class ProviderResponse(BaseModel):
    id: int
    provider_id: str
    name: str
    provider_type: str
    network_status: str
    model_config = ConfigDict(from_attributes=True)

class ClaimResponse(BaseModel):
    id: int
    claim_id: str
    patient_member_id: str
    provider_id: str
    service_date: str
    claim_status: str
    amount: float
    cpt_codes: List[str]
    icd_codes: List[str]
    model_config = ConfigDict(from_attributes=True)
