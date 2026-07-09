from __future__ import annotations
from datetime import datetime

from app.application.agents.provider_contract_agent import ProviderContractAgent
from app.application.graphs.workflow_state import WorkflowState


def run(state: WorkflowState) -> WorkflowState:
    """Execute ProviderContractAgent and append its output to WorkflowState.agent_outputs.

    Thin wrapper that reuses existing deterministic logic. No DB writes.
    """
    try:
        agent = ProviderContractAgent()
        context = state.context_packs.get("provider_contract_context", {})

        output = agent.run(state.case_id, context)
        payload = output.model_dump() if hasattr(output, "model_dump") else dict(output)
        state.agent_outputs.append(payload)
        return state
    except Exception as e:  # pragma: no cover - surface errors to state
        state.errors.append({"node": "provider_node", "error": str(e)})
        return state
