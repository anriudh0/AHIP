from __future__ import annotations
from datetime import datetime
from typing import Any

from app.application.context.context_builder import HealthcareContextBuilder
from app.application.graphs.workflow_state import WorkflowState


def run(state: WorkflowState) -> WorkflowState:
    """Build context packs and attach them to WorkflowState.

    This is a thin wrapper around the existing HealthcareContextBuilder.
    """
    started_at = datetime.utcnow().isoformat()
    try:
        builder = HealthcareContextBuilder()
        case_id = state.case_id

        # Build the canonical context packs (no DB session provided here)
        claim_context = builder.build_claim_context(case_id, None)
        patient_context = builder.build_patient_journey_context(case_id, None)
        provider_contract_context = builder.build_provider_contract_context(case_id, None)
        compliance_context = builder.build_compliance_context(case_id, None)
        relationship_map = builder.build_relationship_map(case_id, None)

        # Store serializable dicts in the WorkflowState
        state.context_packs = {
            "claim_context": claim_context.model_dump() if hasattr(claim_context, "model_dump") else dict(claim_context),
            "patient_journey_context": patient_context.model_dump() if hasattr(patient_context, "model_dump") else dict(patient_context),
            "provider_contract_context": provider_contract_context if isinstance(provider_contract_context, dict) else dict(provider_contract_context),
            "compliance_context": compliance_context.model_dump() if hasattr(compliance_context, "model_dump") else dict(compliance_context),
            "relationship_map": relationship_map.model_dump() if hasattr(relationship_map, "model_dump") else dict(relationship_map),
        }

        status = "success"
        return state
    except Exception as e:  # pragma: no cover - surface errors to state
        state.errors.append({"node": "context_node", "error": str(e)})
        status = "error"
        return state
    finally:
        state.execution_trace.append(
            {
                "node": "context_node",
                "started_at": started_at,
                "ended_at": datetime.utcnow().isoformat(),
                "status": status,
            }
        )
