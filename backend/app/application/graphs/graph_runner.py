"""Stateless synchronous graph runner skeleton.

Checkpoint 1: provides a minimal runner implementation that can be expanded
in later checkpoints. The runner does not import node implementations yet.
"""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from app.application.graphs.workflow_state import WorkflowState
from app.application.graphs.workflow_graph import NODE_SEQUENCE, GRAPH_VERSION
import importlib
from datetime import datetime
from typing import Any


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

        This runner executes the node wrappers in `NODE_SEQUENCE` in order.
        Each node module must expose a `run(state: WorkflowState) -> WorkflowState` function.
        Execution is synchronous and stateless: state is passed between nodes.
        If a node raises an exception, the error is recorded and execution stops.
        """
        start = datetime.utcnow()
        state.execution_trace.append({"node": "graph_start", "started_at": start.isoformat(), "status": "started"})

        for node_name in self.node_sequence:
            node_started = datetime.utcnow()
            trace_entry = {"node": node_name, "started_at": node_started.isoformat(), "ended_at": None, "status": None}
            try:
                # import node module dynamically from app.application.graphs.nodes
                module_path = f"app.application.graphs.nodes.{node_name}"
                module = importlib.import_module(module_path)

                # Each node exposes `run(state)` and returns WorkflowState
                state = module.run(state)
                trace_entry["ended_at"] = datetime.utcnow().isoformat()
                trace_entry["status"] = "success"
                state.execution_trace.append(trace_entry)
            except Exception as e:  # pragma: no cover - runtime error handling
                trace_entry["ended_at"] = datetime.utcnow().isoformat()
                trace_entry["status"] = "error"
                trace_entry["error"] = str(e)
                state.execution_trace.append(trace_entry)
                # record error and stop execution
                state.errors.append({"node": node_name, "error": str(e)})
                break

        end = datetime.utcnow()
        state.execution_trace.append({"node": "graph_end", "ended_at": end.isoformat(), "status": "completed"})
        return state
