from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.domain.entities.models import AgentExecution, AgentMemory
from app.domain.schemas.schemas import AgentOutput

class BaseHealthcareAgent(ABC):
    agent_name: str

    def execute(self, case_id: str, context: dict, db: Session | None = None) -> AgentOutput:
        output = self.run(case_id, context)
        if db is not None:
            self._persist_execution(db, output)
        return output

    @abstractmethod
    def run(self, case_id: str, context: dict) -> AgentOutput:
        raise NotImplementedError

    def _persist_execution(self, db: Session, output: AgentOutput) -> None:
        output_payload = output.model_dump()
        db.add(
            AgentExecution(
                case_id=output.case_id,
                agent_name=output.agent_name,
                output=output_payload,
            )
        )
        db.add(
            AgentMemory(
                case_id=output.case_id,
                agent_name=output.agent_name,
                observation=output.observation,
                recommendation=output.recommendation,
                evidence={"items": output.evidence},
                confidence=output.confidence,
            )
        )
