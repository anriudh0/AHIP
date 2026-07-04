import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.v1.routes.agents import override_recommendation, update_recommendation_status
from app.application.agents.orchestrator import WorkflowOrchestrator
from app.application.governance.governance_service import GovernanceService
from app.domain.entities.models import AgentExecution, AuditLog, Base, SharedCaseMemory
from app.domain.schemas.schemas import ManualOverrideRequest, RecommendationStatusUpdate


def _db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_recommendation_status_update_writes_audit_log():
    db = _db_session()
    WorkflowOrchestrator().run_case_review("CASE-GOV-001", db)

    response = update_recommendation_status(
        RecommendationStatusUpdate(case_id="CASE-GOV-001", status="ACCEPTED"),
        db,
        "Compliance Officer",
    )
    audit_logs = db.scalars(select(AuditLog)).all()
    memory_row = db.scalars(select(SharedCaseMemory)).first()

    assert response == {"case_id": "CASE-GOV-001", "status": "ACCEPTED"}
    assert memory_row.consolidated_output["decision_status"] == "ACCEPTED"
    assert audit_logs[0].event_type == "RECOMMENDATION_ACCEPTED"
    assert audit_logs[0].actor_role == "Compliance Officer"
    db.close()


def test_manual_override_requires_reason():
    db = _db_session()
    WorkflowOrchestrator().run_case_review("CASE-GOV-002", db)

    with pytest.raises(HTTPException) as exc_info:
        override_recommendation(
            ManualOverrideRequest(case_id="CASE-GOV-002", reason=" "),
            db,
            "Compliance Officer",
        )

    assert exc_info.value.status_code == 400
    db.close()


def test_manual_override_rejects_non_governance_role():
    db = _db_session()
    WorkflowOrchestrator().run_case_review("CASE-GOV-RBAC", db)

    with pytest.raises(HTTPException) as exc_info:
        override_recommendation(
            ManualOverrideRequest(case_id="CASE-GOV-RBAC", reason="Valid operational reason."),
            db,
            "Claims Analyst",
        )

    assert exc_info.value.status_code == 403
    db.close()


def test_manual_override_updates_status_and_audit_details():
    db = _db_session()
    WorkflowOrchestrator().run_case_review("CASE-GOV-003", db)

    response = override_recommendation(
        ManualOverrideRequest(case_id="CASE-GOV-003", reason="Provider documentation received.", actor_name="Analyst One"),
        db,
        "Compliance Officer",
    )
    audit_log = db.scalars(select(AuditLog)).first()
    memory_row = db.scalars(select(SharedCaseMemory)).first()

    assert response["status"] == "OVERRIDDEN"
    assert memory_row.consolidated_output["decision_status"] == "OVERRIDDEN"
    assert audit_log.details["reason"] == "Provider documentation received."
    assert audit_log.actor_name == "Analyst One"
    db.close()


def test_rbac_allows_governance_roles_only():
    service = GovernanceService()

    assert service.can_access_governance("Compliance Officer") is True
    assert service.can_access_governance("Operations Analyst") is True
    assert service.can_access_governance("Claims Analyst") is False


def test_agent_execution_history_remains_traceable():
    db = _db_session()
    WorkflowOrchestrator().run_case_review("CASE-GOV-004", db)

    executions = db.scalars(select(AgentExecution)).all()

    assert {execution.agent_name for execution in executions} == {
        "Patient Journey Agent",
        "Claims Review Agent",
        "Provider Contract Agent",
        "Consolidator Agent",
    }
    db.close()
