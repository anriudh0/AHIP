from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class WorkflowState:
    workflow_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    graph_version: str = "v1"
    graph_mode: str = "stateless_langgraph"
    case_id: Optional[str] = None
    domain_input: Dict[str, Any] = field(default_factory=dict)
    shared_context: Dict[str, Any] = field(default_factory=dict)
    context_packs: Dict[str, Any] = field(default_factory=dict)
    agent_outputs: List[Dict[str, Any]] = field(default_factory=list)
    recommendation: Optional[Dict[str, Any]] = None
    explanation: List[str] = field(default_factory=list)
    audit_reference: Optional[Dict[str, Any]] = None
    execution_trace: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    # Routing metadata (Stage 3.1)
    route_flags: Dict[str, Any] = field(default_factory=dict)
    route_decisions: Dict[str, Any] = field(default_factory=dict)
    selected_route: Optional[str] = None
    route_reason: Optional[str] = None
    executed_path: List[str] = field(default_factory=list)
    skipped_agents: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable dict representation of the state."""
        result = asdict(self)
        # Convert datetimes in trace if any
        for entry in result.get("execution_trace", []):
            for k, v in list(entry.items()):
                if isinstance(v, datetime):
                    entry[k] = v.isoformat()
        return result
