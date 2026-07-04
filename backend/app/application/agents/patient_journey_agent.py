from app.application.agents.base_agent import BaseHealthcareAgent
from app.domain.schemas.schemas import AgentOutput

class PatientJourneyAgent(BaseHealthcareAgent):
    agent_name = "Patient Journey Agent"

    def run(self, case_id: str, context: dict) -> AgentOutput:
        events = context.get("events", [])
        return AgentOutput(
            agent_name=self.agent_name,
            case_id=case_id,
            risk_level="Medium" if "CLAIM_PENDED" in events else "Low",
            observation="Patient journey is currently at claim review stage.",
            recommendation="Monitor claim review progress and assign next workflow action.",
            evidence=[f"Events: {', '.join(events)}"],
            confidence=0.70,
            next_owner="Healthcare Operations Analyst",
        )
