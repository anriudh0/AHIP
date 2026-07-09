from __future__ import annotations
from datetime import datetime
from typing import List, Dict

from app.application.decision.risk_scoring import RiskScoringService
from app.application.graphs.workflow_state import WorkflowState


def run(state: WorkflowState) -> WorkflowState:
    """Run deterministic risk scoring over agent outputs and consolidated output.

    This wrapper calls the existing `RiskScoringService` and appends explainability notes
    into `state.explanation`, and augments `state.recommendation` with risk metadata.
    """
    started_at = datetime.utcnow().isoformat()
    try:
        scorer = RiskScoringService()

        # Build inputs similar to RecommendationEngine._agent_outputs_from_memory
        outputs: List[Dict] = []
        for out in state.agent_outputs:
            outputs.append(
                {
                    "agent_name": out.get("agent_name"),
                    "risk_level": out.get("risk_level", "Low"),
                    "recommendation": out.get("recommendation", "No recommendation supplied."),
                }
            )

        # Append consolidated output if present
        if state.recommendation:
            outputs.append(
                {
                    "agent_name": state.recommendation.get("agent_name", "Consolidator Agent"),
                    "risk_level": state.recommendation.get("risk_level", "Low"),
                    "recommendation": state.recommendation.get("recommendation", "No recommendation supplied."),
                }
            )

        score_result = scorer.score(outputs)

        # Merge scoring results into state
        state.explanation = (state.explanation or []) + score_result.get("explainability_notes", [])
        if state.recommendation is None:
            state.recommendation = {}
        state.recommendation["risk_level"] = score_result.get("risk_level")
        state.recommendation["risk_score"] = score_result.get("score")

        status = "success"
        return state
    except Exception as e:  # pragma: no cover - surface errors to state
        state.errors.append({"node": "risk_node", "error": str(e)})
        status = "error"
        return state
    finally:
        state.execution_trace.append(
            {
                "node": "risk_node",
                "started_at": started_at,
                "ended_at": datetime.utcnow().isoformat(),
                "status": status,
            }
        )
