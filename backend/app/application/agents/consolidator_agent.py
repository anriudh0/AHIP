from app.domain.schemas.schemas import ConsolidatedCaseOutput, SharedCaseMemoryState


class ConsolidatorAgent:
    agent_name = "Consolidator Agent"

    def run(self, case_id: str, shared_memory: SharedCaseMemoryState) -> ConsolidatedCaseOutput:
        risk_level = self._highest_risk(shared_memory.risk_levels)
        next_owner = self._next_owner(shared_memory)
        observations = [
            observation["observation"]
            for observation in shared_memory.observations
            if observation.get("observation")
        ]
        evidence = [
            f"{observation['agent_name']}: {observation['observation']}"
            for observation in shared_memory.observations
        ]

        return ConsolidatedCaseOutput(
            case_id=case_id,
            risk_level=risk_level,
            observation=" | ".join(observations) if observations else "No agent observations were recorded.",
            recommendation=self._recommendation(risk_level, next_owner),
            evidence=evidence,
            confidence=0.82 if risk_level == "High" else 0.76 if risk_level == "Medium" else 0.70,
            next_owner=next_owner,
            contributing_agents=shared_memory.agent_sequence,
        )

    def _highest_risk(self, risk_levels: list[str]) -> str:
        priority = {"High": 3, "Medium": 2, "Low": 1}
        return max(risk_levels or ["Low"], key=lambda risk: priority.get(risk, 0))

    def _next_owner(self, shared_memory: SharedCaseMemoryState) -> str:
        if "Provider Contract Analyst" in shared_memory.next_owners and "High" in shared_memory.risk_levels:
            return "Provider Contract Analyst"
        if "Claims Analyst" in shared_memory.next_owners:
            return "Claims Analyst"
        if shared_memory.next_owners:
            return shared_memory.next_owners[-1]
        return "Healthcare Operations Analyst"

    def _recommendation(self, risk_level: str, next_owner: str) -> str:
        if risk_level == "High":
            return f"Escalate consolidated case review to {next_owner} with all agent evidence attached."
        if risk_level == "Medium":
            return f"Coordinate follow-up with {next_owner} and monitor unresolved workflow signals."
        return "Continue standard workflow monitoring with no immediate escalation."
