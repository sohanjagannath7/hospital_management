from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import Provider, User
from app.schemas import ProviderOut, ProviderCreate, ProviderStatusUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get("/", response_model=list[ProviderOut])
async def list_providers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Provider).options(selectinload(Provider.user))
    )
    return result.scalars().all()


@router.get("/available", response_model=list[ProviderOut])
async def get_available_providers(
    care_level: str = None,
    specialty: str = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Provider).where(Provider.status == "available").options(selectinload(Provider.user))
    if specialty:
        query = query.where(Provider.specialty.ilike(f"%{specialty}%"))
    result = await db.execute(query)
    providers = result.scalars().all()
    if care_level:
        providers = [p for p in providers if care_level in (p.available_care_levels or [])]
    return providers


@router.get("/me", response_model=ProviderOut)
async def get_my_provider_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Provider).where(Provider.user_id == current_user.id).options(selectinload(Provider.user))
    )
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider profile not found")
    return provider


@router.put("/me", response_model=ProviderOut)
async def update_provider_profile(
    data: ProviderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Provider).where(Provider.user_id == current_user.id).options(selectinload(Provider.user))
    )
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider profile not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(provider, field, value)
    await db.commit()
    await db.refresh(provider)
    return provider


@router.put("/me/status", response_model=ProviderOut)
async def update_status(
    data: ProviderStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Provider).where(Provider.user_id == current_user.id).options(selectinload(Provider.user))
    )
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    provider.status = data.status
    await db.commit()
    await db.refresh(provider)
    return provider
