from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.application.agents.claims_review_agent import ClaimsReviewAgent
from app.application.agents.orchestrator import WorkflowOrchestrator
from app.application.agents.patient_journey_agent import PatientJourneyAgent
from app.application.agents.provider_contract_agent import ProviderContractAgent
from app.domain.entities.models import AgentExecution, AgentMemory
from app.infrastructure.database.session import Base


def test_agents_return_required_structured_output():
    case_id = "CASE-001"
    outputs = [
        PatientJourneyAgent().run(case_id, {"events": ["CLAIM_SUBMITTED", "CLAIM_PENDED"]}),
        ClaimsReviewAgent().run(case_id, {"claim": {"claim_status": "Pended", "reason": "Missing authorization"}}),
        ProviderContractAgent().run(case_id, {"contract": {"status": "Missing"}}),
    ]

    for output in outputs:
        payload = output.model_dump()
        assert payload["agent_name"]
        assert payload["case_id"] == case_id
        assert payload["risk_level"] in {"Low", "Medium", "High"}
        assert payload["observation"]
        assert payload["recommendation"]
        assert payload["evidence"]
        assert 0 <= payload["confidence"] <= 1
        assert payload["next_owner"]


def test_agents_apply_deterministic_business_rules():
    assert PatientJourneyAgent().run("CASE-002", {"events": ["CLAIM_PENDED"]}).risk_level == "Medium"
    assert ClaimsReviewAgent().run("CASE-002", {"claim": {"claim_status": "Pended"}}).risk_level == "High"
    assert ProviderContractAgent().run("CASE-002", {"contract": {"status": "Missing"}}).risk_level == "High"


def test_orchestrator_persists_agent_execution_history():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as db:
        result = WorkflowOrchestrator().run_case_review("CASE-003", db)

        executions = db.scalars(select(AgentExecution)).all()
        memories = db.scalars(select(AgentMemory)).all()

    assert result["case_id"] == "CASE-003"
    assert len(result["agent_outputs"]) == 3
    assert len(executions) == 3
    assert len(memories) == 3
    assert {execution.agent_name for execution in executions} == {
        "Patient Journey Agent",
        "Claims Review Agent",
        "Provider Contract Agent",
    }
    assert all(execution.output["case_id"] == "CASE-003" for execution in executions)
