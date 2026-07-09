"""Deterministic routing logic for Stage 3.1.

This module exposes a single function `select_route(state)` which inspects
the `WorkflowState.context_packs` and returns (selected_route, route_reason, route_flags).

The routing rules are intentionally simple and deterministic so they can be
used without changing business logic elsewhere.
"""
from __future__ import annotations
from typing import Tuple, Dict

from app.application.graphs.workflow_state import WorkflowState


def _get_claim_context(state: WorkflowState) -> dict:
    return state.context_packs.get("claim_context", {})


def _get_patient_context(state: WorkflowState) -> dict:
    return state.context_packs.get("patient_journey_context", {})


def select_route(state: WorkflowState) -> Tuple[str, str, Dict[str, bool]]:
    """Select a deterministic route for the workflow state.

    Returns a tuple: (selected_route, route_reason, route_flags)

    Routes (priority order):
    - Missing Data Route: if any required context is missing (patient, claim, provider)
    - Provider Contract Route: if a provider exists but contract_status == 'Missing'
    - High Value Claim Route: if claim amount >= 1000
    - Standard Route: default fallback (standard risk / normal claim)
    """
    claim_ctx = _get_claim_context(state)
    patient_ctx = _get_patient_context(state)

    # Default flags
    flags = {
        "has_missing_data": False,
        "missing_items": False,
        "provider_contract_missing": False,
        "high_value_claim": False,
    }

    # Detect missing context
    missing_list = claim_ctx.get("missing_context") if isinstance(claim_ctx.get("missing_context"), list) else []
    # Consider only missing required entities as missing data (claim, patient, provider).
    required_missing = set(missing_list) & {"claim", "patient", "provider"}
    contract_only_missing = False
    if required_missing:
        flags["has_missing_data"] = True
        flags["missing_items"] = True
    else:
        # If only 'contract' is missing, treat as provider contract scenario, not missing data
        if "contract" in missing_list:
            contract_only_missing = True

    # Check explicit presence of fields as additional safety (these indicate missing entities)
    if not claim_ctx.get("claim_id") or claim_ctx.get("claim_status") == "Unknown":
        flags["has_missing_data"] = True
    if not claim_ctx.get("provider_id"):
        flags["has_missing_data"] = True
    if not patient_ctx.get("patient_member_id"):
        flags["has_missing_data"] = True

    # Provider contract missing
    contract_status = claim_ctx.get("contract_status")
    if contract_status and isinstance(contract_status, str) and contract_status.lower() == "missing":
        flags["provider_contract_missing"] = True
    # Also treat explicit contract-only missing context as provider_contract signal
    if contract_only_missing:
        flags["provider_contract_missing"] = True

    # High value check
    try:
        amount = claim_ctx.get("amount")
        if amount is not None and float(amount) >= 1000.0:
            flags["high_value_claim"] = True
    except Exception:
        # Ignore coercion errors; treat as not high value
        pass

    # Decide route by priority
    if flags["has_missing_data"]:
        selected = "missing_data"
        # prefer reporting concrete required entities if present
        reason = f"Missing required context: {list(required_missing) or missing_list or 'unknown'}"
    elif flags["provider_contract_missing"]:
        selected = "provider_contract"
        reason = "Provider contract is missing or incomplete"
    elif flags["high_value_claim"]:
        selected = "high_value_claim"
        reason = f"Claim amount {claim_ctx.get('amount')} meets high-value threshold"
    else:
        # Standard route (normal claim, standard risk, amount below threshold)
        selected = "standard"
        reason = "Default standard route: normal claim and standard risk"

    # Build simple route_decisions for debugging/inspection (no state mutation)
    route_flags = {k: v for k, v in flags.items()}

    return selected, reason, route_flags
