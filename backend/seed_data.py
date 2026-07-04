from sqlalchemy.orm import Session
from app.infrastructure.database.session import SessionLocal, engine
from app.domain.entities.models import Base, Patient, Provider, ProviderContract, BenefitPlan, Claim, WorkflowEvent, CareTask
from app.infrastructure.database.session import init_db
import json

def seed():
    # Only drop and recreate tables if this script is responsible for it (usually alembic does it, but for seed we can rely on existing tables)
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    init_db()
    
    db: Session = SessionLocal()
    
    # 1. Clear existing data
    db.query(AgentMemory).delete() if 'AgentMemory' in globals() else None
    db.query(AgentExecution).delete() if 'AgentExecution' in globals() else None
    db.query(WorkflowEvent).delete()
    db.query(CareTask).delete()
    db.query(Claim).delete()
    db.query(ProviderContract).delete()
    db.query(Provider).delete()
    db.query(BenefitPlan).delete()
    db.query(Patient).delete()
    
    # 2. Add Benefit Plans
    plan_a = BenefitPlan(plan_id="PLAN_A_GOLD", name="Gold PPO", auth_required=True)
    plan_b = BenefitPlan(plan_id="PLAN_B_SILVER", name="Silver HMO", auth_required=False)
    db.add_all([plan_a, plan_b])
    
    # 3. Add Patients
    p1 = Patient(member_id="MEM1001", name="Alice Smith", plan_id="PLAN_A_GOLD", status="Active", risk_category="Standard")
    p2 = Patient(member_id="MEM1002", name="Bob Jones", plan_id="PLAN_A_GOLD", status="Active", risk_category="High")
    p3 = Patient(member_id="MEM1003", name="Charlie Brown", plan_id="PLAN_B_SILVER", status="Active", risk_category="Standard")
    p4 = Patient(member_id="MEM1004", name="Diana Prince", plan_id="PLAN_B_SILVER", status="Inactive", risk_category="Standard")
    p5 = Patient(member_id="MEM1005", name="Evan Wright", plan_id="PLAN_A_GOLD", status="Active", risk_category="Medium")
    db.add_all([p1, p2, p3, p4, p5])
    
    # 4. Add Providers
    prov1 = Provider(provider_id="NPI1000001", name="Dr. Gregory House", provider_type="Specialist", network_status="In-Network")
    prov2 = Provider(provider_id="NPI1000002", name="Mercy Hospital", provider_type="Facility", network_status="In-Network")
    prov3 = Provider(provider_id="NPI1000003", name="Dr. John Watson", provider_type="Primary Care", network_status="Out-of-Network")
    db.add_all([prov1, prov2, prov3])
    db.flush()

    # 5. Add Provider Contracts
    contract1 = ProviderContract(contract_id="CON-001", provider_id="NPI1000001", status="Active")
    contract2 = ProviderContract(contract_id="CON-002", provider_id="NPI1000002", status="Active")
    # prov3 (Dr. Watson) has no active contract (Scenario 1 Setup)
    db.add_all([contract1, contract2])
    
    # 6. Add Claims
    # Scenario 1: Claim pended (missing contract for prov3)
    c1 = Claim(claim_id="CLM2001", patient_member_id="MEM1001", provider_id="NPI1000003", service_date="2023-10-01", claim_status="Pended", amount=250.00, cpt_codes=["99213"], icd_codes=["J01.90"])
    
    # Scenario 2: Missing prior auth (PLAN_A_GOLD requires auth, but none is provided in context)
    c2 = Claim(claim_id="CLM2002", patient_member_id="MEM1002", provider_id="NPI1000001", service_date="2023-10-05", claim_status="Submitted", amount=1500.00, cpt_codes=["43239"], icd_codes=["K21.9"])
    
    # Normal claims
    c3 = Claim(claim_id="CLM2003", patient_member_id="MEM1003", provider_id="NPI1000002", service_date="2023-10-10", claim_status="Paid", amount=450.00, cpt_codes=["99283"], icd_codes=["R07.9"])
    c4 = Claim(claim_id="CLM2004", patient_member_id="MEM1005", provider_id="NPI1000001", service_date="2023-10-12", claim_status="Paid", amount=120.00, cpt_codes=["99213"], icd_codes=["E11.9"])
    c5 = Claim(claim_id="CLM2005", patient_member_id="MEM1001", provider_id="NPI1000002", service_date="2023-10-15", claim_status="Submitted", amount=3500.00, cpt_codes=["27447"], icd_codes=["M17.11"])
    db.add_all([c1, c2, c3, c4, c5])
    
    # 7. Add Care Tasks (Scenario 3: Overdue care gap)
    task1 = CareTask(patient_id="MEM1002", due_date="2023-09-01", status="Open", owner="Care Coordinator") # Overdue
    task2 = CareTask(patient_id="MEM1005", due_date="2023-12-01", status="Open", owner="Care Coordinator")
    db.add_all([task1, task2])

    # 8. Add Workflow Events
    event1 = WorkflowEvent(case_id="CLM2001", event_type="CLAIM_SUBMITTED", payload={"status": "Pended", "reason": "Missing Contract"})
    event2 = WorkflowEvent(case_id="MEM1002_TASK", event_type="CARE_TASK_OVERDUE", payload={"task_id": "task1"})
    db.add_all([event1, event2])
    
    db.commit()
    db.close()
    print("Database seeded successfully with MVP Scenarios 1 and 3!")

if __name__ == "__main__":
    seed()
