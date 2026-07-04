from sqlalchemy.orm import Session

from app.application.decision.risk_scoring import RiskScoringService
from app.domain.entities.models import SharedCaseMemory
from app.domain.schemas.schemas import DecisionRecommendation, PriorityQueueResponse


class RecommendationEngine:
    def __init__(self, risk_scoring_service: RiskScoringService | None = None):
        self.risk_scoring_service = risk_scoring_service or RiskScoringService()

    def build_priority_queue(self, db: Session) -> PriorityQueueResponse:
        memory_rows = (
            db.query(SharedCaseMemory)
            .order_by(SharedCaseMemory.created_at.desc(), SharedCaseMemory.id.desc())
            .all()
        )
        recommendations = [self.build_recommendation(row) for row in memory_rows]
        recommendations.sort(key=lambda item: item.risk_score, reverse=True)
        return PriorityQueueResponse(recommendations=recommendations)

    def build_recommendation(self, memory_row: SharedCaseMemory) -> DecisionRecommendation:
        consolidated_output = memory_row.consolidated_output or {}
        memory = memory_row.memory or {}
        agent_outputs = self._agent_outputs_from_memory(memory, consolidated_output)
        score_result = self.risk_scoring_service.score(agent_outputs)
        risk_score = score_result["score"]
        risk_level = score_result["risk_level"]
        escalation_owner = self._escalation_owner(risk_level, consolidated_output)

        return DecisionRecommendation(
            case_id=memory_row.case_id,
            risk_level=risk_level,
            risk_score=risk_score,
            priority=self._priority(risk_score),
            escalation_owner=escalation_owner,
            recommendation=consolidated_output.get("recommendation", "Continue standard workflow monitoring."),
            explainability_notes=score_result["explainability_notes"]
            + [f"Escalation owner selected by deterministic rule: {escalation_owner}."],
            source_agents=consolidated_output.get("contributing_agents", memory.get("agent_sequence", [])),
        )

    def _agent_outputs_from_memory(self, memory: dict, consolidated_output: dict) -> list[dict]:
        agent_sequence = memory.get("agent_sequence", [])
        risk_levels = memory.get("risk_levels", [])
        recommendations = memory.get("recommendations", [])
        outputs = [
            {
                "agent_name": agent_name,
                "risk_level": risk_levels[index] if index < len(risk_levels) else "Low",
                "recommendation": recommendations[index] if index < len(recommendations) else "No recommendation supplied.",
            }
            for index, agent_name in enumerate(agent_sequence)
        ]
        if consolidated_output:
            outputs.append(
                {
                    "agent_name": consolidated_output.get("agent_name", "Consolidator Agent"),
                    "risk_level": consolidated_output.get("risk_level", "Low"),
                    "recommendation": consolidated_output.get("recommendation", "No recommendation supplied."),
                }
            )
        return outputs

    def _escalation_owner(self, risk_level: str, consolidated_output: dict) -> str:
        owner = consolidated_output.get("next_owner") or "Healthcare Operations Analyst"
        if risk_level in {"High", "Critical"}:
            return owner
        if risk_level == "Medium":
            return owner
        return "Healthcare Operations Analyst"

    def _priority(self, risk_score: int) -> str:
        if risk_score >= 4:
            return "Critical"
        if risk_score == 3:
            return "High"
        if risk_score == 2:
            return "Medium"
        return "Low"
