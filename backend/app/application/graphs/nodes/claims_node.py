from __future__ import annotations
from datetime import datetime

from app.application.agents.claims_review_agent import ClaimsReviewAgent
from app.application.graphs.workflow_state import WorkflowState


def run(state: WorkflowState) -> WorkflowState:
    """Execute ClaimsReviewAgent and append its output to WorkflowState.agent_outputs.

    Thin wrapper reusing deterministic agent logic. No persistence.
    """
    started_at = datetime.utcnow().isoformat()
    try:
        agent = ClaimsReviewAgent()
        context = state.context_packs.get("claim_context", {})

        output = agent.run(state.case_id, context)
        payload = output.model_dump() if hasattr(output, "model_dump") else dict(output)
        state.agent_outputs.append(payload)
        status = "success"
        return state
    except Exception as e:  # pragma: no cover - surface errors to state
        state.errors.append({"node": "claims_node", "error": str(e)})
        status = "error"
        return state
    finally:
        state.execution_trace.append(
            {
                "node": "claims_node",
                "started_at": started_at,
                "ended_at": datetime.utcnow().isoformat(),
                "status": status,
            }
        )
