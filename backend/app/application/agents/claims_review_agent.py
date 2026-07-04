from app.application.agents.base_agent import BaseHealthcareAgent
from app.domain.schemas.schemas import AgentOutput

class ClaimsReviewAgent(BaseHealthcareAgent):
    agent_name = "Claims Review Agent"

    def run(self, case_id: str, context: dict) -> AgentOutput:
        context_payload = context.model_dump() if hasattr(context, "model_dump") else context or {}
        claim = context_payload.get("claim") or {}
        status = context_payload.get("claim_status") or claim.get("claim_status", "Unknown")
        reason = claim.get("reason") or ", ".join(context_payload.get("missing_context", [])) or "Not available"
        is_pended = status == "Pended"
        return AgentOutput(
            agent_name=self.agent_name,
            case_id=case_id,
            risk_level="High" if is_pended else "Low",
            observation=f"Claim status is {status}.",
            recommendation="Review missing claim context and blocking reason." if is_pended else "No immediate claim action required.",
            evidence=[f"Claim status: {status}", f"Reason: {reason}"],
            confidence=0.80,
            next_owner="Claims Analyst",
        )
