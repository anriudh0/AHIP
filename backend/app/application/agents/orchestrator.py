from app.application.context.context_builder import HealthcareContextBuilder
from app.application.agents.claims_review_agent import ClaimsReviewAgent
from app.application.agents.provider_contract_agent import ProviderContractAgent
from app.application.agents.patient_journey_agent import PatientJourneyAgent
from sqlalchemy.orm import Session

class WorkflowOrchestrator:
    def __init__(self):
        self.context_builder = HealthcareContextBuilder()

    def run_case_review(self, case_id: str, db: Session | None = None) -> dict:
        outputs = [
            PatientJourneyAgent().execute(case_id, self.context_builder.build_patient_journey_context(case_id, db), db).model_dump(),
            ClaimsReviewAgent().execute(case_id, self.context_builder.build_claim_context(case_id, db), db).model_dump(),
            ProviderContractAgent().execute(case_id, self.context_builder.build_claim_context(case_id, db), db).model_dump(),
        ]
        if db is not None:
            db.commit()
        return {
            "case_id": case_id,
            "agent_outputs": outputs,
            "summary": "Phase 2 deterministic agent review completed."
        }
