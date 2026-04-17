from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional
from app.database import get_db
from app.models import TriageCase, CaseAssignment, CaseOutcome, CaseStatus, Provider, User, Alert
from app.schemas import TriageCaseOut, CaseOutcomeCreate, AlertOut
from app.auth import get_current_user

router = APIRouter(prefix="/cases", tags=["Case Management"])


@router.get("/", response_model=list[TriageCaseOut])
async def list_cases(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    care_level: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role.value not in ("admin", "doctor", "nurse"):
        raise HTTPException(status_code=403, detail="Not authorized")

    query = select(TriageCase).options(
        selectinload(TriageCase.assessment),
        selectinload(TriageCase.recommendations),
    )
    if status:
        query = query.where(TriageCase.status == status)
    if severity:
        query = query.where(TriageCase.severity == severity)
    if care_level:
        query = query.where(TriageCase.care_level == care_level)

    query = query.order_by(TriageCase.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/{case_id}/assign/{provider_id}", response_model=TriageCaseOut)
async def assign_case(
    case_id: int,
    provider_id: int,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role.value not in ("admin", "nurse"):
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(select(TriageCase).where(TriageCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    result = await db.execute(select(Provider).where(Provider.id == provider_id))
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    existing = await db.execute(select(CaseAssignment).where(CaseAssignment.case_id == case_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Case already assigned")

    assignment = CaseAssignment(case_id=case_id, provider_id=provider_id, notes=notes)
    db.add(assignment)
    case.status = CaseStatus.assigned
    provider.current_load += 1
    await db.commit()

    result = await db.execute(
        select(TriageCase).where(TriageCase.id == case_id)
        .options(selectinload(TriageCase.assessment), selectinload(TriageCase.recommendations))
    )
    return result.scalar_one()


@router.put("/{case_id}/status")
async def update_case_status(
    case_id: int,
    new_status: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role.value not in ("admin", "doctor", "nurse"):
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await db.execute(select(TriageCase).where(TriageCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    case.status = new_status
    await db.commit()
    return {"message": "Status updated"}


@router.post("/{case_id}/outcome")
async def record_outcome(
    case_id: int,
    data: CaseOutcomeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role.value not in ("doctor", "admin"):
        raise HTTPException(status_code=403, detail="Not authorized")

    result = await db.execute(select(TriageCase).where(TriageCase.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    outcome = CaseOutcome(case_id=case_id, **data.model_dump())
    db.add(outcome)
    case.status = CaseStatus.completed
    await db.commit()
    return {"message": "Outcome recorded"}


@router.get("/alerts/active", response_model=list[AlertOut])
async def get_active_alerts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role.value not in ("admin", "doctor", "nurse"):
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await db.execute(
        select(Alert).where(Alert.is_acknowledged == False).order_by(Alert.created_at.desc()).limit(50)
    )
    return result.scalars().all()


@router.put("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_acknowledged = True
    alert.acknowledged_by = current_user.id
    await db.commit()
    return {"message": "Alert acknowledged"}
