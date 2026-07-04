from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.domain.schemas.schemas import AgentRunRequest
from app.application.agents.orchestrator import WorkflowOrchestrator
from app.infrastructure.database.session import get_db

router = APIRouter()

@router.post("/run-case-review")
def run_case_review(request: AgentRunRequest, db: Session = Depends(get_db)):
    return WorkflowOrchestrator().run_case_review(request.case_id, db)
