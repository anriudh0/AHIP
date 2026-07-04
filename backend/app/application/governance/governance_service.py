from sqlalchemy.orm import Session

from app.domain.entities.models import AuditLog, SharedCaseMemory


class GovernanceService:
    allowed_roles = {"Compliance Officer", "Operations Analyst", "Claims Analyst", "Provider Analyst"}
    governance_roles = {"Compliance Officer", "Operations Analyst"}

    def resolve_role(self, role: str | None) -> str:
        if role in self.allowed_roles:
            return role
        return "Operations Analyst"

    def can_access_governance(self, role: str | None) -> bool:
        return self.resolve_role(role) in self.governance_roles

    def log_event(
        self,
        db: Session,
        event_type: str,
        actor_role: str,
        case_id: str | None = None,
        actor_name: str | None = None,
        details: dict | None = None,
    ) -> AuditLog:
        audit_log = AuditLog(
            event_type=event_type,
            case_id=case_id,
            actor_role=self.resolve_role(actor_role),
            actor_name=actor_name,
            details=details or {},
        )
        db.add(audit_log)
        return audit_log

    def update_recommendation_status(self, db: Session, case_id: str, status: str) -> SharedCaseMemory | None:
        memory_row = db.query(SharedCaseMemory).filter(SharedCaseMemory.case_id == case_id).order_by(SharedCaseMemory.id.desc()).first()
        if memory_row is None:
            return None
        consolidated_output = dict(memory_row.consolidated_output or {})
        consolidated_output["decision_status"] = status
        memory_row.consolidated_output = consolidated_output
        return memory_row

    def governance_summary(self, db: Session) -> dict:
        events = db.query(AuditLog).all()
        recommendations = db.query(SharedCaseMemory).all()
        return {
            "total_audit_events": len(events),
            "overridden_recommendations": sum(1 for row in recommendations if (row.consolidated_output or {}).get("decision_status") == "OVERRIDDEN"),
            "accepted_recommendations": sum(1 for row in recommendations if (row.consolidated_output or {}).get("decision_status") == "ACCEPTED"),
            "pending_recommendations": sum(1 for row in recommendations if not (row.consolidated_output or {}).get("decision_status")),
        }
