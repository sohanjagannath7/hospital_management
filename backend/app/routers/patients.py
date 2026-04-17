from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import Patient, MedicalHistory, User
from app.schemas import PatientOut, PatientCreate, MedicalHistoryCreate, MedicalHistoryOut
from app.auth import get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/me", response_model=PatientOut)
async def get_my_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Patient)
        .where(Patient.user_id == current_user.id)
        .options(selectinload(Patient.user), selectinload(Patient.medical_history))
    )
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    return patient


@router.put("/me", response_model=PatientOut)
async def update_my_profile(data: PatientCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Patient).where(Patient.user_id == current_user.id)
        .options(selectinload(Patient.user), selectinload(Patient.medical_history))
    )
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)
    await db.commit()
    await db.refresh(patient)
    return patient


@router.get("/me/history", response_model=MedicalHistoryOut)
async def get_medical_history(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Patient).where(Patient.user_id == current_user.id).options(selectinload(Patient.medical_history))
    )
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not patient.medical_history:
        history = MedicalHistory(patient_id=patient.id)
        db.add(history)
        await db.commit()
        await db.refresh(history)
        return history
    return patient.medical_history


@router.put("/me/history", response_model=MedicalHistoryOut)
async def update_medical_history(data: MedicalHistoryCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Patient).where(Patient.user_id == current_user.id).options(selectinload(Patient.medical_history))
    )
    patient = result.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if not patient.medical_history:
        history = MedicalHistory(patient_id=patient.id, **data.model_dump())
        db.add(history)
    else:
        for field, value in data.model_dump().items():
            setattr(patient.medical_history, field, value)
        history = patient.medical_history

    await db.commit()
    await db.refresh(history)
    return history


@router.get("/", response_model=list[PatientOut])
async def list_patients(
    skip: int = 0, limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role.value not in ("admin", "doctor", "nurse"):
        raise HTTPException(status_code=403, detail="Not authorized")
    result = await db.execute(
        select(Patient).options(selectinload(Patient.user)).offset(skip).limit(limit)
    )
    return result.scalars().all()
