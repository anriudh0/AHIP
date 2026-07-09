from __future__ import annotations
from datetime import datetime
from typing import List, Dict

from app.application.agents.consolidator_agent import ConsolidatorAgent
from app.application.graphs.workflow_state import WorkflowState
from app.domain.schemas.schemas import SharedCaseMemoryState


def run(state: WorkflowState) -> WorkflowState:
    """Run the ConsolidatorAgent using a SharedCaseMemoryState built from agent_outputs.

    This wrapper constructs a `SharedCaseMemoryState` from `state.agent_outputs`, calls
    the existing `ConsolidatorAgent`, stores the consolidated output into `state.recommendation`,
    and records execution trace. No persistence is performed here.
    """
    started_at = datetime.utcnow().isoformat()
    try:
        # Build SharedCaseMemoryState from state.agent_outputs
        agent_sequence: List[str] = []
        observations: List[Dict] = []
        risk_levels: List[str] = []
        recommendations: List[str] = []
        next_owners: List[str] = []
        handoffs: List[Dict] = []

        for out in state.agent_outputs:
            name = out.get("agent_name")
            agent_sequence.append(name)
            observations.append({
                "agent_name": name,
                "observation": out.get("observation"),
                "evidence": out.get("evidence", []),
            })
            risk_levels.append(out.get("risk_level"))
            recommendations.append(out.get("recommendation"))
            if out.get("next_owner"):
                next_owners.append(out.get("next_owner"))
            handoffs.append(
                {
                    "from_agent": name,
                    "risk_level": out.get("risk_level"),
                    "next_owner": out.get("next_owner"),
                }
            )

        shared_memory = SharedCaseMemoryState(
            case_id=state.case_id,
            agent_sequence=agent_sequence,
            observations=observations,
            risk_levels=risk_levels,
            recommendations=recommendations,
            next_owners=next_owners,
            handoffs=handoffs,
        )

        consolidator = ConsolidatorAgent()
        consolidated = consolidator.run(state.case_id, shared_memory)

        # Store consolidated output and a serializable shared memory snapshot
        state.recommendation = consolidated.model_dump() if hasattr(consolidated, "model_dump") else dict(consolidated)
        state.shared_context = state.shared_context or {}
        state.shared_context["shared_memory"] = shared_memory.model_dump() if hasattr(shared_memory, "model_dump") else dict(shared_memory)
        state.recommendation.setdefault("confidence", getattr(consolidated, "confidence", None))

        # Explanation will be enriched by the risk node
        state.explanation = state.explanation or []

        status = "success"
        return state
    except Exception as e:  # pragma: no cover - surface errors to state
        state.errors.append({"node": "consolidator_node", "error": str(e)})
        return state
