"""Graph definition and ordering for the stateless workflow runner.

This module defines the canonical node order for the stateless graph.
"""

NODE_SEQUENCE = [
    "context_node",
    "patient_node",
    "claims_node",
    "provider_node",
    "consolidator_node",
    "risk_node",
    "governance_node",
]

GRAPH_VERSION = "v1"
