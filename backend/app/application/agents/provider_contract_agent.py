from app.application.agents.base_agent import BaseHealthcareAgent
from app.domain.schemas.schemas import AgentOutput

class ProviderContractAgent(BaseHealthcareAgent):
    agent_name = "Provider Contract Agent"

    def run(self, case_id: str, context: dict) -> AgentOutput:
        context_payload = context.model_dump() if hasattr(context, "model_dump") else context or {}
        contract = context_payload.get("contract") or {}
        status = context_payload.get("contract_status") or contract.get("status", "Unknown")
        return AgentOutput(
            agent_name=self.agent_name,
            case_id=case_id,
            risk_level="High" if status == "Missing" else "Low",
            observation=f"Provider contract status is {status}.",
            recommendation="Assign to Provider Contract Analyst for contract mapping validation.",
            evidence=[f"Contract status: {status}"],
            confidence=0.85,
            next_owner="Provider Contract Analyst",
        )
