from app.application.context.context_builder import HealthcareContextBuilder
from app.application.agents.claims_review_agent import ClaimsReviewAgent
from app.application.agents.consolidator_agent import ConsolidatorAgent
from app.application.agents.provider_contract_agent import ProviderContractAgent
from app.application.agents.patient_journey_agent import PatientJourneyAgent
from app.domain.entities.models import AgentExecution, SharedCaseMemory
from app.domain.schemas.schemas import SharedCaseMemoryState
from sqlalchemy.orm import Session

class WorkflowOrchestrator:
    def __init__(self):
        self.context_builder = HealthcareContextBuilder()

    def run_case_review(self, case_id: str, db: Session | None = None) -> dict:
        shared_memory = SharedCaseMemoryState(case_id=case_id)
        outputs = []

        pipeline = [
            (PatientJourneyAgent(), self.context_builder.build_patient_journey_context(case_id, db)),
            (ClaimsReviewAgent(), self.context_builder.build_claim_context(case_id, db)),
            (ProviderContractAgent(), self.context_builder.build_claim_context(case_id, db)),
        ]

        for agent, context in pipeline:
            output = agent.execute(case_id, context, db)
            shared_memory.record_agent_output(output)
            outputs.append(output.model_dump())

        consolidated_output = ConsolidatorAgent().run(case_id, shared_memory)
        if db is not None:
            db.add(
                AgentExecution(
                    case_id=case_id,
                    agent_name=consolidated_output.agent_name,
                    output=consolidated_output.model_dump(),
                )
            )
            db.add(
                SharedCaseMemory(
                    case_id=case_id,
                    memory=shared_memory.model_dump(),
                    consolidated_output=consolidated_output.model_dump(),
                )
            )
            db.commit()
        return {
            "case_id": case_id,
            "agent_outputs": outputs,
            "shared_memory": shared_memory.model_dump(),
            "consolidated_output": consolidated_output.model_dump(),
            "summary": "Phase 4 multi-agent collaboration review completed."
        }
