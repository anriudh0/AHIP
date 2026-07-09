from __future__ import annotations
from datetime import datetime
from typing import Any, Dict

from app.application.governance.governance_service import GovernanceService
from app.application.graphs.workflow_state import WorkflowState
from app.infrastructure.database.session import SessionLocal
from app.domain.entities.models import AgentExecution, AgentMemory, SharedCaseMemory


def run(state: WorkflowState) -> WorkflowState:
    """Persist agent executions, consolidator execution, shared memory and write an audit event.

    This wrapper is the only node that touches persistence. It reuses existing DB models
    and `GovernanceService` to keep storage consistent with the orchestrator.
    """
    started_at = datetime.utcnow().isoformat()
    db = SessionLocal()
    governance = GovernanceService()
    try:
        # Persist per-agent executions and memories
        for out in state.agent_outputs:
            db.add(
                AgentExecution(case_id=state.case_id, agent_name=out.get("agent_name"), output=out)
            )
            db.add(
                AgentMemory(
                    case_id=state.case_id,
                    agent_name=out.get("agent_name"),
                    observation=out.get("observation"),
                    recommendation=out.get("recommendation"),
                    evidence={"items": out.get("evidence", [])},
                    confidence=out.get("confidence", 0.0),
                )
            )

        # Persist consolidator execution and shared case memory
        if state.recommendation:
            db.add(
                AgentExecution(case_id=state.case_id, agent_name=state.recommendation.get("agent_name"), output=state.recommendation)
            )

        shared_memory_payload: Dict[str, Any] = state.shared_context.get("shared_memory", {}) if state.shared_context else {}
        db.add(
            SharedCaseMemory(case_id=state.case_id, memory=shared_memory_payload, consolidated_output=state.recommendation or {})
        )

        # Log a governance event for the recommendation creation
        governance.log_event(
            db,
            event_type="RECOMMENDATION_CREATED",
            case_id=state.case_id,
            actor_role="System",
            details={"workflow_id": state.workflow_id},
        )

        db.commit()

        # Return DB references minimally
        state.audit_reference = {"case_id": state.case_id, "workflow_id": state.workflow_id}
        status = "success"
        return state
    except Exception as e:  # pragma: no cover - surface errors to state
        db.rollback()
        state.errors.append({"node": "governance_node", "error": str(e)})
        return state
    finally:
        db.close()
