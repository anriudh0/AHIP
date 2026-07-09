from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.domain.entities.models import AgentExecution, AuditLog
from app.domain.schemas.schemas import AgentRunRequest, ManualOverrideRequest, RecommendationStatusUpdate
from app.application.agents.orchestrator import WorkflowOrchestrator
from app.application.decision.recommendation_engine import RecommendationEngine
from app.application.governance.governance_service import GovernanceService
from app.infrastructure.database.session import get_db
from app.application.graphs.graph_runner import GraphRunner
from app.application.graphs.workflow_state import WorkflowState

router = APIRouter()
governance_service = GovernanceService()

@router.post("/run-case-review")
def run_case_review(request: AgentRunRequest, db: Session = Depends(get_db)):
    return WorkflowOrchestrator().run_case_review(request.case_id, db)


@router.post("/run-graph")
def run_graph(request: AgentRunRequest):
    """Run the stateless graph runner for the provided case_id and return graph metadata.

    This endpoint is additive and does not replace the existing `run-case-review` endpoint.
    """
    runner = GraphRunner()
    state = runner.initialize_state(case_id=request.case_id, domain_input={"case_id": request.case_id})
    final_state = runner.run(state)

    return {
        "graph_mode": final_state.graph_mode,
        "graph_version": final_state.graph_version,
        "workflow_id": final_state.workflow_id,
        "case_id": final_state.case_id,
        "shared_state": final_state.shared_context,
        "agent_trace": final_state.execution_trace,
        "recommendation": final_state.recommendation,
        "explanation": final_state.explanation,
        "audit_reference": final_state.audit_reference,
        # Routing metadata (Stage 3.1)
        "selected_route": final_state.selected_route,
        "route_reason": final_state.route_reason,
        "route_flags": final_state.route_flags,
        "executed_path": final_state.executed_path,
        "skipped_agents": final_state.skipped_agents,
        "comparison_note": "Produced using stateless graph orchestration.",
    }

@router.get("/context/{case_id}")
def get_case_context(case_id: str, db: Session = Depends(get_db)):
    return WorkflowOrchestrator().context_builder.build_case_context(case_id, db)

@router.get("/priority-queue")
def get_priority_queue(db: Session = Depends(get_db)):
    return RecommendationEngine().build_priority_queue(db)

@router.post("/recommendations/status")
def update_recommendation_status(
    request: RecommendationStatusUpdate,
    db: Session = Depends(get_db),
    x_user_role: str | None = Header(default=None),
):
    role = governance_service.resolve_role(x_user_role)
    if not governance_service.can_access_governance(role):
        raise HTTPException(status_code=403, detail="Role is not allowed to update recommendation status.")
    if request.status not in {"PENDING", "ACCEPTED", "OVERRIDDEN"}:
        raise HTTPException(status_code=400, detail="Unsupported recommendation status.")

    memory_row = governance_service.update_recommendation_status(db, request.case_id, request.status)
    if memory_row is None:
        raise HTTPException(status_code=404, detail="Recommendation not found for case.")

    governance_service.log_event(
        db,
        event_type=f"RECOMMENDATION_{request.status}",
        case_id=request.case_id,
        actor_role=role,
        details={"status": request.status},
    )
    db.commit()
    return {"case_id": request.case_id, "status": request.status}

@router.post("/recommendations/override")
def override_recommendation(
    request: ManualOverrideRequest,
    db: Session = Depends(get_db),
    x_user_role: str | None = Header(default=None),
):
    role = governance_service.resolve_role(x_user_role)
    if not governance_service.can_access_governance(role):
        raise HTTPException(status_code=403, detail="Role is not allowed to override recommendations.")
    reason = request.reason.strip()
    if not reason:
        raise HTTPException(status_code=400, detail="Override reason is required.")

    memory_row = governance_service.update_recommendation_status(db, request.case_id, "OVERRIDDEN")
    if memory_row is None:
        raise HTTPException(status_code=404, detail="Recommendation not found for case.")

    governance_service.log_event(
        db,
        event_type="RECOMMENDATION_OVERRIDDEN",
        case_id=request.case_id,
        actor_role=role,
        actor_name=request.actor_name,
        details={"reason": reason},
    )
    db.commit()
    return {"case_id": request.case_id, "status": "OVERRIDDEN", "reason": reason}

@router.get("/audit-logs")
def list_audit_logs(
    db: Session = Depends(get_db),
    x_user_role: str | None = Header(default=None),
):
    if not governance_service.can_access_governance(x_user_role):
        raise HTTPException(status_code=403, detail="Role is not allowed to access governance audit logs.")
    return db.query(AuditLog).order_by(AuditLog.created_at.desc(), AuditLog.id.desc()).all()

@router.get("/execution-history")
def list_execution_history(
    db: Session = Depends(get_db),
    x_user_role: str | None = Header(default=None),
):
    if not governance_service.can_access_governance(x_user_role):
        raise HTTPException(status_code=403, detail="Role is not allowed to access agent execution history.")
    return db.query(AgentExecution).order_by(AgentExecution.created_at.desc(), AgentExecution.id.desc()).all()

@router.get("/governance-summary")
def get_governance_summary(
    db: Session = Depends(get_db),
    x_user_role: str | None = Header(default=None),
):
    if not governance_service.can_access_governance(x_user_role):
        raise HTTPException(status_code=403, detail="Role is not allowed to access governance summary.")
    return governance_service.governance_summary(db)
