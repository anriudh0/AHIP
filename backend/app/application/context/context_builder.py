class HealthcareContextBuilder:
    def build_claim_context(self, case_id: str) -> dict:
        return {
            "case_id": case_id,
            "claim": {"claim_status": "Pended", "reason": "Provider contract mapping missing"},
            "patient": {"status": "Active", "risk_category": "Standard"},
            "provider": {"network_status": "Unknown"},
            "benefit_plan": {"coverage_status": "Active", "authorization_required": "No"},
        }

    def build_patient_journey_context(self, case_id: str) -> dict:
        return {
            "case_id": case_id,
            "journey_stage": "Claim Review",
            "events": ["CLAIM_SUBMITTED", "CLAIM_PENDED"],
        }

    def build_provider_contract_context(self, case_id: str) -> dict:
        return {
            "case_id": case_id,
            "provider": {"provider_id": "PROV-001"},
            "contract": {"status": "Missing"},
            "claim": {"claim_status": "Pended"},
        }
