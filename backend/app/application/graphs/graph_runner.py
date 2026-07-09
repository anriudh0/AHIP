"""Stateless synchronous graph runner skeleton.

Checkpoint 1: provides a minimal runner implementation that can be expanded
in later checkpoints. The runner does not import node implementations yet.
"""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from app.application.graphs.workflow_state import WorkflowState
from app.application.graphs.workflow_graph import NODE_SEQUENCE, GRAPH_VERSION
from app.application.graphs.router import select_route
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

        # Execute the context node first, then select route
        if "context_node" in self.node_sequence:
            node_name = "context_node"
            node_started = datetime.utcnow()
            trace_entry = {"node": node_name, "started_at": node_started.isoformat(), "ended_at": None, "status": None}
            try:
                module = importlib.import_module(f"app.application.graphs.nodes.{node_name}")
                state = module.run(state)
                trace_entry["ended_at"] = datetime.utcnow().isoformat()
                trace_entry["status"] = "success"
                state.execution_trace.append(trace_entry)
                state.executed_path.append(node_name)
            except Exception as e:  # pragma: no cover - runtime error handling
                trace_entry["ended_at"] = datetime.utcnow().isoformat()
                trace_entry["status"] = "error"
                trace_entry["error"] = str(e)
                state.execution_trace.append(trace_entry)
                state.errors.append({"node": node_name, "error": str(e)})
                # If context failed, stop execution
                end = datetime.utcnow()
                state.execution_trace.append({"node": "graph_end", "ended_at": end.isoformat(), "status": "aborted"})
                return state

            # Decide route based on the built context
            selected, reason, flags = select_route(state)
            state.selected_route = selected
            state.route_reason = reason
            state.route_flags = flags

            # Define route-specific ordered node lists (full sequences including context)
            route_map = {
                "standard": NODE_SEQUENCE,
                "high_value_claim": [
                    "context_node",
                    "claims_node",
                    "risk_node",
                    "provider_node",
                    "consolidator_node",
                    "governance_node",
                ],
                "provider_contract": [
                    "context_node",
                    "provider_node",
                    "claims_node",
                    "consolidator_node",
                    "risk_node",
                    "governance_node",
                ],
                "missing_data": [
                    "context_node",
                    "governance_node",
                ],
            }

            execution_list = route_map.get(selected, NODE_SEQUENCE)

            # Nodes intentionally skipped due to route selection
            all_nodes = list(self.node_sequence)
            skipped = [n for n in all_nodes if n not in execution_list]
            state.skipped_agents = [{"agent": n, "reason": f"Skipped because route {selected}"} for n in skipped]

            # Execute remaining nodes in the chosen execution_list (skip the first since context already ran)
            remaining = execution_list[1:]
        else:
            # Fallback: no context node defined, use original sequence
            remaining = list(self.node_sequence)

        for node_name in remaining:
            node_started = datetime.utcnow()
            trace_entry = {"node": node_name, "started_at": node_started.isoformat(), "ended_at": None, "status": None}
            try:
                module_path = f"app.application.graphs.nodes.{node_name}"
                module = importlib.import_module(module_path)

                state = module.run(state)
                trace_entry["ended_at"] = datetime.utcnow().isoformat()
                trace_entry["status"] = "success"
                state.execution_trace.append(trace_entry)
                state.executed_path.append(node_name)
            except Exception as e:  # pragma: no cover - runtime error handling
                trace_entry["ended_at"] = datetime.utcnow().isoformat()
                trace_entry["status"] = "error"
                trace_entry["error"] = str(e)
                state.execution_trace.append(trace_entry)
                state.errors.append({"node": node_name, "error": str(e)})
                break

        end = datetime.utcnow()
        state.execution_trace.append({"node": "graph_end", "ended_at": end.isoformat(), "status": "completed"})
        return state
