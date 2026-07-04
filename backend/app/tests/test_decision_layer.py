from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.application.agents.orchestrator import WorkflowOrchestrator
from app.application.decision.recommendation_engine import RecommendationEngine
from app.application.decision.risk_scoring import RiskScoringService
from app.domain.entities.models import Base, SharedCaseMemory


def _db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_risk_scoring_returns_numeric_score_and_explainability_notes():
    result = RiskScoringService().score(
        [
            {"agent_name": "Claims Review Agent", "risk_level": "High", "recommendation": "Manual review"},
            {"agent_name": "Patient Journey Agent", "risk_level": "Medium", "recommendation": "Monitor"},
        ]
    )

    assert result["risk_level"] == "High"
    assert result["score"] == 3
    assert result["explainability_notes"]
    assert "Claims Review Agent reported High risk" in result["explainability_notes"][1]


def test_priority_queue_orders_highest_risk_first_and_includes_reasons():
    db = _db_session()
    db.add(
        SharedCaseMemory(
            case_id="LOW-CASE",
            memory={
                "agent_sequence": ["Patient Journey Agent"],
                "risk_levels": ["Low"],
                "recommendations": ["Continue monitoring"],
            },
            consolidated_output={
                "agent_name": "Consolidator Agent",
                "case_id": "LOW-CASE",
                "risk_level": "Low",
                "recommendation": "Continue standard workflow monitoring.",
                "next_owner": "Healthcare Operations Analyst",
                "contributing_agents": ["Patient Journey Agent"],
            },
        )
    )
    db.add(
        SharedCaseMemory(
            case_id="HIGH-CASE",
            memory={
                "agent_sequence": ["Claims Review Agent"],
                "risk_levels": ["High"],
                "recommendations": ["Review missing claim context"],
            },
            consolidated_output={
                "agent_name": "Consolidator Agent",
                "case_id": "HIGH-CASE",
                "risk_level": "High",
                "recommendation": "Escalate consolidated case review.",
                "next_owner": "Claims Analyst",
                "contributing_agents": ["Claims Review Agent"],
            },
        )
    )
    db.commit()

    result = RecommendationEngine().build_priority_queue(db)

    assert [item.case_id for item in result.recommendations] == ["HIGH-CASE", "LOW-CASE"]
    assert result.recommendations[0].risk_score == 3
    assert result.recommendations[0].priority == "High"
    assert result.recommendations[0].escalation_owner == "Claims Analyst"
    assert result.recommendations[0].explainability_notes
    db.close()


def test_run_case_review_remains_compatible_with_decision_layer():
    db = _db_session()
    result = WorkflowOrchestrator().run_case_review("CASE-005", db)

    assert result["case_id"] == "CASE-005"
    assert "agent_outputs" in result
    assert "consolidated_output" in result
    assert len(result["agent_outputs"]) == 3
    db.close()
