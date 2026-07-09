"""Stateless synchronous graph runner skeleton.

Checkpoint 1: provides a minimal runner implementation that can be expanded
in later checkpoints. The runner does not import node implementations yet.
"""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from app.application.graphs.workflow_state import WorkflowState
from app.application.graphs.workflow_graph import NODE_SEQUENCE, GRAPH_VERSION


class GraphRunner:
    def __init__(self, node_sequence: Optional[List[str]] = None):
        self.node_sequence = node_sequence or NODE_SEQUENCE
        self.graph_version = GRAPH_VERSION

    def initialize_state(self, case_id: str, domain_input: dict | None = None) -> WorkflowState:
        state = WorkflowState(
            graph_version=self.graph_version,
            graph_mode="stateless_langgraph",
            case_id=case_id,
            domain_input=domain_input or {},
            metadata={"initialized_at": datetime.utcnow().isoformat()},
        )
        return state

    def run(self, state: WorkflowState) -> WorkflowState:
        """Execute nodes sequentially.

        Checkpoint 1: this runner only records high-level start/end trace entries.
        Node execution will be added in later checkpoints.
        """
        start = datetime.utcnow()
        state.execution_trace.append(
            {"node": "graph_start", "started_at": start.isoformat(), "status": "started"}
        )

        # Placeholder for node execution loop — nodes will be invoked in later checkpoints.
        for node_name in self.node_sequence:
            # record that node would execute (no-op for checkpoint 1)
            state.execution_trace.append(
                {"node": node_name, "started_at": None, "ended_at": None, "status": "skipped_checkpoint_1"}
            )

        end = datetime.utcnow()
        state.execution_trace.append({"node": "graph_end", "ended_at": end.isoformat(), "status": "completed"})
        return state
