from app.application.agents.base_agent import BaseHealthcareAgent
from app.domain.schemas.schemas import AgentOutput

class ClaimsReviewAgent(BaseHealthcareAgent):
    agent_name = "Claims Review Agent"

    def run(self, case_id: str, context: dict) -> AgentOutput:
        claim = context.get("claim", {})
        status = claim.get("claim_status", "Unknown")
        is_pended = status == "Pended"
        return AgentOutput(
            agent_name=self.agent_name,
            case_id=case_id,
            risk_level="High" if is_pended else "Low",
            observation=f"Claim status is {status}.",
            recommendation="Review missing claim context and blocking reason." if is_pended else "No immediate claim action required.",
            evidence=[f"Claim status: {status}", f"Reason: {claim.get('reason', 'Not available')}"],
            confidence=0.80,
            next_owner="Claims Analyst",
        )
