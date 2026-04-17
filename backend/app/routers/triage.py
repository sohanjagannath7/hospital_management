import random
import string
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import (
    TriageCase, TriageAssessment, Recommendation, Alert, Patient, MedicalHistory,
    CaseStatus, SeverityLevel, CareLevel, User
)
from app.schemas import TriageCaseCreate, TriageCaseOut
from app.auth import get_current_user
from app.agents.triage_orchestrator import run_triage

router = APIRouter(prefix="/triage", tags=["Triage"])


def generate_case_number() -> str:
    return "TC-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


@router.post("/submit", response_model=TriageCaseOut, status_code=201)
async def submit_triage(
    data: TriageCaseCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Patient).where(Patient.user_id == current_user.id)
        .options(selectinload(Patient.medical_history))
    )
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found. Please complete your profile first.")

    vitals_dict = data.vital_signs.model_dump() if data.vital_signs else None

    case = TriageCase(
        case_number=generate_case_number(),
        patient_id=patient.id,
        chief_complaint=data.chief_complaint,
        symptoms=data.symptoms,
        symptom_duration=data.symptom_duration,
        pain_scale=data.pain_scale,
        vital_signs=vitals_dict,
        onset_description=data.onset_description,
        status=CaseStatus.triaging,
    )
    db.add(case)
    await db.flush()

    history_dict = None
    if patient.medical_history:
        mh = patient.medical_history
        history_dict = {
            "chronic_conditions": mh.chronic_conditions or [],
            "allergies": mh.allergies or [],
            "current_medications": mh.current_medications or [],
            "past_surgeries": mh.past_surgeries or [],
        }

    try:
        assessment_data = await run_triage(
            chief_complaint=data.chief_complaint,
            symptoms=data.symptoms,
            symptom_duration=data.symptom_duration,
            pain_scale=data.pain_scale,
            vital_signs=vitals_dict,
            onset_description=data.onset_description,
            medical_history=history_dict,
        )

        severity_map = {
            "ESI-1": SeverityLevel.esi_1, "ESI-2": SeverityLevel.esi_2,
            "ESI-3": SeverityLevel.esi_3, "ESI-4": SeverityLevel.esi_4,
            "ESI-5": SeverityLevel.esi_5,
        }
        care_map = {
            "Emergency Room": CareLevel.emergency,
            "Urgent Care": CareLevel.urgent_care,
            "Primary Care": CareLevel.primary_care,
            "Telehealth": CareLevel.telehealth,
            "Mental Health": CareLevel.mental_health,
            "Specialist": CareLevel.specialist,
            "Self Care": CareLevel.self_care,
        }

        case.severity = severity_map.get(assessment_data["severity"], SeverityLevel.esi_3)
        case.care_level = care_map.get(assessment_data["care_level"], CareLevel.urgent_care)
        case.is_emergency = assessment_data["is_emergency"]
        case.status = CaseStatus.triaged

        assessment = TriageAssessment(
            case_id=case.id,
            symptom_analysis=assessment_data["symptom_analysis"],
            possible_conditions=assessment_data["possible_conditions"],
            severity_reasoning=assessment_data["severity_reasoning"],
            risk_factors=assessment_data["risk_factors"],
            drug_interactions=assessment_data["drug_interactions"],
            routing_reasoning=assessment_data["routing_reasoning"],
            confidence_score=assessment_data["confidence_score"],
            agent_version="1.0",
            processing_time_ms=assessment_data["processing_time_ms"],
        )
        db.add(assessment)

        for rec in assessment_data.get("recommendations", []):
            db.add(Recommendation(
                case_id=case.id,
                recommendation_type=rec.get("type", "consultation"),
                title=rec.get("title", ""),
                description=rec.get("description", ""),
                priority=rec.get("priority", "medium"),
            ))

        if assessment_data["is_emergency"]:
            db.add(Alert(
                case_id=case.id,
                alert_type="emergency",
                message=f"EMERGENCY: {data.chief_complaint} — ESI-1/2 triage. Immediate attention required.",
            ))

        if assessment_data["drug_interactions"]:
            for interaction in assessment_data["drug_interactions"]:
                if interaction.get("severity") in ("contraindicated", "major"):
                    db.add(Alert(
                        case_id=case.id,
                        alert_type="drug_interaction",
                        message=f"Drug Interaction Alert: {interaction.get('description', 'Interaction detected')}",
                    ))

    except Exception as e:
        case.status = CaseStatus.triaged
        case.severity = SeverityLevel.esi_3

    await db.commit()

    result = await db.execute(
        select(TriageCase)
        .where(TriageCase.id == case.id)
        .options(
            selectinload(TriageCase.assessment),
            selectinload(TriageCase.recommendations),
            selectinload(TriageCase.assignment),
        )
    )
    return result.scalar_one()


@router.get("/my-cases", response_model=list[TriageCaseOut])
async def get_my_cases(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Patient).where(Patient.user_id == current_user.id))
    patient = result.scalar_one_or_none()
    if not patient:
        return []

    result = await db.execute(
        select(TriageCase)
        .where(TriageCase.patient_id == patient.id)
        .options(
            selectinload(TriageCase.assessment),
            selectinload(TriageCase.recommendations),
        )
        .order_by(TriageCase.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{case_id}", response_model=TriageCaseOut)
async def get_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TriageCase)
        .where(TriageCase.id == case_id)
        .options(
            selectinload(TriageCase.assessment),
            selectinload(TriageCase.recommendations),
        )
    )
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
