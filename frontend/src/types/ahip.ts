export type DashboardSummary = {
  open_cases: number
  high_risk_cases: number
  claim_exceptions: number
  provider_contract_issues: number
  compliance_gaps: number
}

export type GovernanceSummary = {
  total_audit_events: number
  overridden_recommendations: number
  accepted_recommendations: number
  pending_recommendations: number
}

export type DecisionRecommendation = {
  case_id: string
  risk_level: string
  risk_score: number
  priority: string
  escalation_owner: string
  recommendation: string
  explainability_notes: string[]
  source_agents: string[]
}

export type PriorityQueueResponse = {
  recommendations: DecisionRecommendation[]
}

export type AgentOutput = {
  agent_name: string
  case_id: string
  risk_level: string
  observation: string
  recommendation: string
  evidence: string[]
  confidence: number
  next_owner?: string | null
}

export type ConsolidatedCaseOutput = {
  agent_name: string
  case_id: string
  risk_level: string
  observation: string
  recommendation: string
  evidence: string[]
  confidence: number
  next_owner?: string | null
  contributing_agents: string[]
}

export type SharedMemoryState = {
  case_id: string
  agent_sequence: string[]
  observations: Array<{ agent_name: string; observation: string; evidence: string[] }>
  risk_levels: string[]
  recommendations: string[]
  next_owners: string[]
  handoffs: Array<{ from_agent: string; risk_level: string; next_owner?: string | null }>
}

export type WorkflowRunResponse = {
  case_id: string
  agent_outputs: AgentOutput[]
  shared_memory: SharedMemoryState
  consolidated_output: ConsolidatedCaseOutput
  summary: string
}

export type AuditLog = {
  id: number
  event_type: string
  case_id?: string | null
  actor_role: string
  actor_name?: string | null
  details: Record<string, unknown>
  created_at: string
}

export type RelationshipNode = {
  id: string
  type: string
  label: string
  attributes?: Record<string, unknown>
}

export type RelationshipEdge = {
  source: string
  target: string
  relationship: string
}

export type RelationshipMap = {
  case_id: string
  nodes: RelationshipNode[]
  edges: RelationshipEdge[]
  generated_at?: string
  explanation: string[]
}

export type ClaimContextPack = {
  case_id: string
  claim_id?: string | null
  claim_status: string
  amount?: number | null
  service_date?: string | null
  cpt_codes: string[]
  icd_codes: string[]
  patient_member_id?: string | null
  patient_status: string
  patient_risk_category: string
  provider_id?: string | null
  provider_network_status: string
  benefit_plan_id?: string | null
  benefit_plan_name?: string | null
  authorization_required?: boolean | null
  contract_status: string
  missing_context: string[]
}

export type PatientJourneyContextPack = {
  case_id: string
  patient_member_id?: string | null
  patient_status: string
  patient_risk_category: string
  journey_stage: string
  events: string[]
  open_care_tasks: Array<Record<string, unknown>>
  related_claim_ids: string[]
  missing_context: string[]
}

export type ComplianceContextPack = {
  case_id: string
  claim_id?: string | null
  claim_status: string
  cpt_codes: string[]
  icd_codes: string[]
  authorization_required?: boolean | null
  contract_status: string
  provider_network_status: string
  documentation_signals: string[]
  missing_context: string[]
}

export type CaseContextResponse = {
  case_id: string
  claim_context: ClaimContextPack
  patient_journey_context: PatientJourneyContextPack
  compliance_context: ComplianceContextPack
  relationship_map: RelationshipMap
}

export type AgentExecution = {
  id: number
  case_id: string
  agent_name: string
  output: Record<string, unknown>
  created_at: string
}
