from datetime import datetime

from sqlalchemy.orm import Session

from app.domain.entities.models import (
    BenefitPlan,
    CareTask,
    Claim,
    Patient,
    Provider,
    ProviderContract,
    WorkflowEvent,
)
from app.domain.schemas.context_schemas import (
    CaseContextResponse,
    CaseRelationshipMap,
    ClaimContextPack,
    ComplianceContextPack,
    PatientJourneyContextPack,
    RelationshipEdge,
    RelationshipNode,
)


class HealthcareContextBuilder:
    def build_claim_context(self, case_id: str, db: Session | None = None) -> ClaimContextPack:
        if db is None:
            return ClaimContextPack(
                case_id=case_id,
                claim_status="Pended",
                patient_status="Active",
                patient_risk_category="Standard",
                provider_network_status="Unknown",
                contract_status="Missing",
            )

        claim = self._find_claim(db, case_id)
        patient = self._find_patient(db, claim.patient_member_id) if claim else None
        provider = self._find_provider(db, claim.provider_id) if claim else None
        plan = self._find_plan(db, patient.plan_id) if patient else None
        contract = self._find_contract(db, provider.provider_id) if provider else None
        missing_context = self._missing_context(
            claim=claim,
            patient=patient,
            provider=provider,
            benefit_plan=plan,
            contract=contract,
        )

        return ClaimContextPack(
            case_id=case_id,
            claim_id=claim.claim_id if claim else None,
            claim_status=claim.claim_status if claim else "Unknown",
            amount=claim.amount if claim else None,
            service_date=claim.service_date if claim else None,
            cpt_codes=claim.cpt_codes if claim else [],
            icd_codes=claim.icd_codes if claim else [],
            patient_member_id=patient.member_id if patient else (claim.patient_member_id if claim else None),
            patient_status=patient.status if patient else "Unknown",
            patient_risk_category=patient.risk_category if patient else "Unknown",
            provider_id=provider.provider_id if provider else (claim.provider_id if claim else None),
            provider_network_status=provider.network_status if provider else "Unknown",
            benefit_plan_id=plan.plan_id if plan else (patient.plan_id if patient else None),
            benefit_plan_name=plan.name if plan else None,
            authorization_required=plan.auth_required if plan else None,
            contract_status=contract.status if contract else "Missing" if provider else "Unknown",
            missing_context=missing_context,
        )

    def build_patient_journey_context(
        self, case_id: str, db: Session | None = None
    ) -> PatientJourneyContextPack:
        if db is None:
            return PatientJourneyContextPack(
                case_id=case_id,
                patient_status="Active",
                patient_risk_category="Standard",
                journey_stage="Claim Review",
                events=["CLAIM_SUBMITTED", "CLAIM_PENDED"],
            )

        claim = self._find_claim(db, case_id)
        patient_id = claim.patient_member_id if claim else case_id
        patient = self._find_patient(db, patient_id)
        events = self._find_events(db, case_id)
        tasks = self._find_tasks(db, patient.member_id) if patient else []
        related_claims = self._find_patient_claims(db, patient.member_id) if patient else []
        missing_context = []
        if patient is None:
            missing_context.append("patient")

        event_types = [event.event_type for event in events]
        journey_stage = self._journey_stage(claim.claim_status if claim else None, event_types)

        return PatientJourneyContextPack(
            case_id=case_id,
            patient_member_id=patient.member_id if patient else (claim.patient_member_id if claim else None),
            patient_status=patient.status if patient else "Unknown",
            patient_risk_category=patient.risk_category if patient else "Unknown",
            journey_stage=journey_stage,
            events=event_types,
            open_care_tasks=[
                {"due_date": task.due_date, "status": task.status, "owner": task.owner}
                for task in tasks
                if task.status == "Open"
            ],
            related_claim_ids=[related_claim.claim_id for related_claim in related_claims],
            missing_context=missing_context,
        )

    def build_provider_contract_context(self, case_id: str, db: Session | None = None) -> dict:
        claim_context = self.build_claim_context(case_id, db)
        return {
            "case_id": case_id,
            "provider": {
                "provider_id": claim_context.provider_id,
                "network_status": claim_context.provider_network_status,
            },
            "contract": {"status": claim_context.contract_status},
            "claim": {"claim_status": claim_context.claim_status},
            "missing_context": claim_context.missing_context,
        }

    def build_compliance_context(
        self, case_id: str, db: Session | None = None
    ) -> ComplianceContextPack:
        claim_context = self.build_claim_context(case_id, db)
        documentation_signals = []
        if not claim_context.cpt_codes:
            documentation_signals.append("missing_cpt_codes")
        if not claim_context.icd_codes:
            documentation_signals.append("missing_icd_codes")

        return ComplianceContextPack(
            case_id=case_id,
            claim_id=claim_context.claim_id,
            claim_status=claim_context.claim_status,
            cpt_codes=claim_context.cpt_codes,
            icd_codes=claim_context.icd_codes,
            authorization_required=claim_context.authorization_required,
            contract_status=claim_context.contract_status,
            provider_network_status=claim_context.provider_network_status,
            documentation_signals=documentation_signals,
            missing_context=claim_context.missing_context,
        )

    def build_relationship_map(self, case_id: str, db: Session | None = None) -> CaseRelationshipMap:
        claim_context = self.build_claim_context(case_id, db)
        patient_context = self.build_patient_journey_context(case_id, db)
        nodes: list[RelationshipNode] = [
            RelationshipNode(id=case_id, type="case", label=f"Case {case_id}"),
        ]
        edges: list[RelationshipEdge] = []
        explanation = ["Relationship map is built from existing AHIP relational entities."]

        if claim_context.claim_id:
            nodes.append(
                RelationshipNode(
                    id=claim_context.claim_id,
                    type="claim",
                    label=f"Claim {claim_context.claim_id}",
                    attributes={"status": claim_context.claim_status},
                )
            )
            edges.append(RelationshipEdge(source=case_id, target=claim_context.claim_id, relationship="reviews_claim"))

        if patient_context.patient_member_id:
            nodes.append(
                RelationshipNode(
                    id=patient_context.patient_member_id,
                    type="patient",
                    label=f"Patient {patient_context.patient_member_id}",
                    attributes={"status": patient_context.patient_status},
                )
            )
            edges.append(
                RelationshipEdge(
                    source=claim_context.claim_id or case_id,
                    target=patient_context.patient_member_id,
                    relationship="belongs_to_patient",
                )
            )

        if claim_context.provider_id:
            nodes.append(
                RelationshipNode(
                    id=claim_context.provider_id,
                    type="provider",
                    label=f"Provider {claim_context.provider_id}",
                    attributes={"network_status": claim_context.provider_network_status},
                )
            )
            edges.append(
                RelationshipEdge(
                    source=claim_context.claim_id or case_id,
                    target=claim_context.provider_id,
                    relationship="submitted_by_provider",
                )
            )

        if claim_context.benefit_plan_id:
            nodes.append(
                RelationshipNode(
                    id=claim_context.benefit_plan_id,
                    type="benefit_plan",
                    label=f"Benefit Plan {claim_context.benefit_plan_id}",
                    attributes={"authorization_required": claim_context.authorization_required},
                )
            )
            if patient_context.patient_member_id:
                edges.append(
                    RelationshipEdge(
                        source=patient_context.patient_member_id,
                        target=claim_context.benefit_plan_id,
                        relationship="enrolled_in_plan",
                    )
                )

        if claim_context.provider_id:
            contract_id = f"contract:{claim_context.provider_id}"
            nodes.append(
                RelationshipNode(
                    id=contract_id,
                    type="provider_contract",
                    label=f"Contract for {claim_context.provider_id}",
                    attributes={"status": claim_context.contract_status},
                )
            )
            edges.append(
                RelationshipEdge(
                    source=claim_context.provider_id,
                    target=contract_id,
                    relationship="has_contract_status",
                )
            )

        for index, task in enumerate(patient_context.open_care_tasks, start=1):
            task_id = f"{patient_context.patient_member_id}:care_task:{index}"
            nodes.append(
                RelationshipNode(
                    id=task_id,
                    type="care_task",
                    label=f"Care Task {index}",
                    attributes=task,
                )
            )
            if patient_context.patient_member_id:
                edges.append(
                    RelationshipEdge(
                        source=patient_context.patient_member_id,
                        target=task_id,
                        relationship="has_open_care_task",
                    )
                )

        return CaseRelationshipMap(
            case_id=case_id,
            nodes=nodes,
            edges=edges,
            generated_at=datetime.utcnow(),
            explanation=explanation,
        )

    def build_case_context(self, case_id: str, db: Session | None = None) -> CaseContextResponse:
        return CaseContextResponse(
            case_id=case_id,
            claim_context=self.build_claim_context(case_id, db),
            patient_journey_context=self.build_patient_journey_context(case_id, db),
            compliance_context=self.build_compliance_context(case_id, db),
            relationship_map=self.build_relationship_map(case_id, db),
        )

    def _find_claim(self, db: Session, case_id: str) -> Claim | None:
        return db.query(Claim).filter(Claim.claim_id == case_id).first()

    def _find_patient(self, db: Session, member_id: str | None) -> Patient | None:
        if member_id is None:
            return None
        return db.query(Patient).filter(Patient.member_id == member_id).first()

    def _find_provider(self, db: Session, provider_id: str | None) -> Provider | None:
        if provider_id is None:
            return None
        return db.query(Provider).filter(Provider.provider_id == provider_id).first()

    def _find_plan(self, db: Session, plan_id: str | None) -> BenefitPlan | None:
        if plan_id is None:
            return None
        return db.query(BenefitPlan).filter(BenefitPlan.plan_id == plan_id).first()

    def _find_contract(self, db: Session, provider_id: str | None) -> ProviderContract | None:
        if provider_id is None:
            return None
        return db.query(ProviderContract).filter(ProviderContract.provider_id == provider_id).first()

    def _find_events(self, db: Session, case_id: str) -> list[WorkflowEvent]:
        return db.query(WorkflowEvent).filter(WorkflowEvent.case_id == case_id).all()

    def _find_tasks(self, db: Session, patient_id: str) -> list[CareTask]:
        return db.query(CareTask).filter(CareTask.patient_id == patient_id).all()

    def _find_patient_claims(self, db: Session, patient_id: str) -> list[Claim]:
        return db.query(Claim).filter(Claim.patient_member_id == patient_id).all()

    def _missing_context(self, **entities) -> list[str]:
        return [name for name, entity in entities.items() if entity is None]

    def _journey_stage(self, claim_status: str | None, events: list[str]) -> str:
        if claim_status == "Pended" or "CLAIM_PENDED" in events:
            return "Claim Review"
        if claim_status in {"Paid", "Denied"}:
            return "Claim Finalized"
        if claim_status:
            return "Claim Intake"
        return "Unknown"
