from datetime import datetime
from pydantic import BaseModel, Field


class ClaimContextPack(BaseModel):
    case_id: str
    claim_id: str | None = None
    claim_status: str = "Unknown"
    amount: float | None = None
    service_date: str | None = None
    cpt_codes: list[str] = Field(default_factory=list)
    icd_codes: list[str] = Field(default_factory=list)
    patient_member_id: str | None = None
    patient_status: str = "Unknown"
    patient_risk_category: str = "Unknown"
    provider_id: str | None = None
    provider_network_status: str = "Unknown"
    benefit_plan_id: str | None = None
    benefit_plan_name: str | None = None
    authorization_required: bool | None = None
    contract_status: str = "Unknown"
    missing_context: list[str] = Field(default_factory=list)


class PatientJourneyContextPack(BaseModel):
    case_id: str
    patient_member_id: str | None = None
    patient_status: str = "Unknown"
    patient_risk_category: str = "Unknown"
    journey_stage: str = "Unknown"
    events: list[str] = Field(default_factory=list)
    open_care_tasks: list[dict] = Field(default_factory=list)
    related_claim_ids: list[str] = Field(default_factory=list)
    missing_context: list[str] = Field(default_factory=list)


class ComplianceContextPack(BaseModel):
    case_id: str
    claim_id: str | None = None
    claim_status: str = "Unknown"
    cpt_codes: list[str] = Field(default_factory=list)
    icd_codes: list[str] = Field(default_factory=list)
    authorization_required: bool | None = None
    contract_status: str = "Unknown"
    provider_network_status: str = "Unknown"
    documentation_signals: list[str] = Field(default_factory=list)
    missing_context: list[str] = Field(default_factory=list)


class RelationshipNode(BaseModel):
    id: str
    type: str
    label: str
    attributes: dict = Field(default_factory=dict)


class RelationshipEdge(BaseModel):
    source: str
    target: str
    relationship: str


class CaseRelationshipMap(BaseModel):
    case_id: str
    nodes: list[RelationshipNode] = Field(default_factory=list)
    edges: list[RelationshipEdge] = Field(default_factory=list)
    generated_at: datetime
    explanation: list[str] = Field(default_factory=list)


class CaseContextResponse(BaseModel):
    case_id: str
    claim_context: ClaimContextPack
    patient_journey_context: PatientJourneyContextPack
    compliance_context: ComplianceContextPack
    relationship_map: CaseRelationshipMap
