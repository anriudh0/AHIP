from app.domain.schemas.schemas import DashboardSummary
from sqlalchemy.orm import Session
from app.domain.entities.models import Claim, Patient, CareTask, ProviderContract

class DashboardService:
    def get_summary(self, db: Session) -> DashboardSummary:
        open_cases = db.query(CareTask).filter(CareTask.status == "Open").count()
        high_risk_cases = db.query(Patient).filter(Patient.risk_category == "High").count()
        claim_exceptions = db.query(Claim).filter(Claim.claim_status == "Pended").count()
        # for simplicity, let's just count total claims, providers etc if we don't have exactly "provider contract issues"
        provider_contract_issues = db.query(ProviderContract).filter(ProviderContract.status == "Inactive").count()
        
        return DashboardSummary(
            open_cases=open_cases,
            high_risk_cases=high_risk_cases,
            claim_exceptions=claim_exceptions,
            provider_contract_issues=provider_contract_issues,
            compliance_gaps=0,
        )
