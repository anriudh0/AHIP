from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.application.context.context_builder import HealthcareContextBuilder
from app.domain.entities.models import (
    Base,
    BenefitPlan,
    CareTask,
    Claim,
    Patient,
    Provider,
    ProviderContract,
    WorkflowEvent,
)


def _db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def _seed_case(db):
    db.add(BenefitPlan(plan_id="PLAN_A_GOLD", name="Gold PPO", auth_required=True))
    db.add(Patient(member_id="MEM1001", name="Alice Smith", plan_id="PLAN_A_GOLD", status="Active", risk_category="Standard"))
    db.add(Provider(provider_id="NPI1000003", name="Dr. John Watson", provider_type="Primary Care", network_status="Out-of-Network"))
    db.add(ProviderContract(contract_id="CON-003", provider_id="NPI1000003", status="Missing"))
    db.add(
        Claim(
            claim_id="CLM2001",
            patient_member_id="MEM1001",
            provider_id="NPI1000003",
            service_date="2023-10-01",
            claim_status="Pended",
            amount=250.00,
            cpt_codes=["99213"],
            icd_codes=["J01.90"],
        )
    )
    db.add(CareTask(patient_id="MEM1001", due_date="2023-09-01", status="Open", owner="Care Coordinator"))
    db.add(WorkflowEvent(case_id="CLM2001", event_type="CLAIM_SUBMITTED", payload={"status": "Pended"}))
    db.add(WorkflowEvent(case_id="CLM2001", event_type="CLAIM_PENDED", payload={"reason": "Missing Contract"}))
    db.commit()


def test_context_builder_creates_agent_specific_context_packs():
    db = _db_session()
    _seed_case(db)
    builder = HealthcareContextBuilder()

    claim_context = builder.build_claim_context("CLM2001", db)
    patient_context = builder.build_patient_journey_context("CLM2001", db)
    compliance_context = builder.build_compliance_context("CLM2001", db)

    assert claim_context.claim_id == "CLM2001"
    assert claim_context.provider_id == "NPI1000003"
    assert claim_context.authorization_required is True
    assert patient_context.events == ["CLAIM_SUBMITTED", "CLAIM_PENDED"]
    assert patient_context.open_care_tasks[0]["owner"] == "Care Coordinator"
    assert compliance_context.contract_status == "Missing"
    assert compliance_context.documentation_signals == []
    db.close()


def test_relationship_mapping_exposes_nodes_and_edges():
    db = _db_session()
    _seed_case(db)
    relationship_map = HealthcareContextBuilder().build_relationship_map("CLM2001", db)

    node_types = {node.type for node in relationship_map.nodes}
    edge_types = {edge.relationship for edge in relationship_map.edges}

    assert {"case", "claim", "patient", "provider", "benefit_plan", "provider_contract", "care_task"}.issubset(node_types)
    assert "submitted_by_provider" in edge_types
    assert "enrolled_in_plan" in edge_types
    assert "has_contract_status" in edge_types
    db.close()


def test_context_builder_handles_missing_context_deterministically():
    db = _db_session()
    builder = HealthcareContextBuilder()

    claim_context = builder.build_claim_context("MISSING-CASE", db)
    patient_context = builder.build_patient_journey_context("MISSING-CASE", db)
    relationship_map = builder.build_relationship_map("MISSING-CASE", db)

    assert claim_context.claim_status == "Unknown"
    assert "claim" in claim_context.missing_context
    assert "patient" in patient_context.missing_context
    assert [node.type for node in relationship_map.nodes] == ["case"]
    db.close()
