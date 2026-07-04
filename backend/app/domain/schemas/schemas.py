from pydantic import BaseModel, ConfigDict, Field
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

class SharedCaseMemoryState(BaseModel):
    case_id: str
    agent_sequence: list[str] = Field(default_factory=list)
    observations: list[dict] = Field(default_factory=list)
    risk_levels: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    next_owners: list[str] = Field(default_factory=list)
    handoffs: list[dict] = Field(default_factory=list)

    def record_agent_output(self, output: AgentOutput) -> None:
        self.agent_sequence.append(output.agent_name)
        self.observations.append(
            {
                "agent_name": output.agent_name,
                "observation": output.observation,
                "evidence": output.evidence,
            }
        )
        self.risk_levels.append(output.risk_level)
        self.recommendations.append(output.recommendation)
        if output.next_owner:
            self.next_owners.append(output.next_owner)
        self.handoffs.append(
            {
                "from_agent": output.agent_name,
                "risk_level": output.risk_level,
                "next_owner": output.next_owner,
            }
        )

class ConsolidatedCaseOutput(BaseModel):
    agent_name: str = "Consolidator Agent"
    case_id: str
    risk_level: str
    observation: str
    recommendation: str
    evidence: list[str]
    confidence: float
    next_owner: str | None = None
    contributing_agents: list[str] = Field(default_factory=list)

class DecisionRecommendation(BaseModel):
    case_id: str
    risk_level: str
    risk_score: int
    priority: str
    escalation_owner: str
    recommendation: str
    explainability_notes: list[str]
    source_agents: list[str] = Field(default_factory=list)

class PriorityQueueResponse(BaseModel):
    recommendations: list[DecisionRecommendation] = Field(default_factory=list)

class RecommendationStatusUpdate(BaseModel):
    case_id: str
    status: str

class ManualOverrideRequest(BaseModel):
    case_id: str
    reason: str
    actor_name: str | None = None

class AuditLogResponse(BaseModel):
    id: int
    event_type: str
    case_id: str | None = None
    actor_role: str
    actor_name: str | None = None
    details: dict
    model_config = ConfigDict(from_attributes=True)

class GovernanceSummary(BaseModel):
    total_audit_events: int
    overridden_recommendations: int
    accepted_recommendations: int
    pending_recommendations: int

class UserRole(BaseModel):
    role: str

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
