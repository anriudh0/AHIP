from __future__ import annotations
from datetime import datetime

from app.application.agents.patient_journey_agent import PatientJourneyAgent
from app.application.graphs.workflow_state import WorkflowState


def run(state: WorkflowState) -> WorkflowState:
    """Execute PatientJourneyAgent and append its output to WorkflowState.agent_outputs.

    This wrapper calls the existing deterministic agent logic and does not persist.
    """
    started_at = datetime.utcnow().isoformat()
    try:
        agent = PatientJourneyAgent()
        context = state.context_packs.get("patient_journey_context", {})

        output = agent.run(state.case_id, context)
        # Pydantic model -> dict
        payload = output.model_dump() if hasattr(output, "model_dump") else dict(output)
        state.agent_outputs.append(payload)
        status = "success"
        return state
    except Exception as e:  # pragma: no cover - surface errors to state
        state.errors.append({"node": "patient_node", "error": str(e)})
        status = "error"
        return state
    finally:
        state.execution_trace.append(
            {
                "node": "patient_node",
                "started_at": started_at,
                "ended_at": datetime.utcnow().isoformat(),
                "status": status,
            }
        )
