from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from collections import Counter
from app.database import get_db
from app.models import TriageCase, CaseOutcome, Provider, User
from app.schemas import AnalyticsSummary
from app.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role.value not in ("admin", "doctor", "nurse"):
        raise HTTPException(status_code=403, detail="Not authorized")

    cases_result = await db.execute(select(TriageCase))
    cases = cases_result.scalars().all()

    total = len(cases)
    pending = sum(1 for c in cases if c.status in ("pending", "triaging", "triaged"))
    active = sum(1 for c in cases if c.status in ("assigned", "in_progress"))
    completed = sum(1 for c in cases if c.status == "completed")
    emergencies = sum(1 for c in cases if c.is_emergency)

    severity_dist: dict = {}
    for c in cases:
        if c.severity:
            key = c.severity.value if hasattr(c.severity, 'value') else str(c.severity)
            severity_dist[key] = severity_dist.get(key, 0) + 1

    care_dist: dict = {}
    for c in cases:
        if c.care_level:
            key = c.care_level.value if hasattr(c.care_level, 'value') else str(c.care_level)
            care_dist[key] = care_dist.get(key, 0) + 1

    complaint_counter: Counter = Counter()
    for c in cases:
        words = c.chief_complaint.lower().split()[:3]
        complaint_counter[" ".join(words)] += 1
    top_complaints = [{"complaint": k, "count": v} for k, v in complaint_counter.most_common(10)]

    providers_result = await db.execute(select(Provider))
    providers = providers_result.scalars().all()
    provider_util = [
        {"id": p.id, "specialty": p.specialty, "current_load": p.current_load, "max_cases": p.max_cases}
        for p in providers
    ]

    hourly: dict = {}
    for c in cases:
        if c.created_at:
            hour = c.created_at.hour
            hourly[hour] = hourly.get(hour, 0) + 1
    hourly_volume = [{"hour": h, "count": hourly.get(h, 0)} for h in range(24)]

    outcomes_result = await db.execute(select(CaseOutcome))
    outcomes = outcomes_result.scalars().all()
    accurate = sum(1 for o in outcomes if o.triage_accuracy is True)
    accuracy_rate = (accurate / len(outcomes) * 100) if outcomes else 0.0

    return AnalyticsSummary(
        total_cases=total,
        pending_cases=pending,
        active_cases=active,
        completed_cases=completed,
        emergency_cases=emergencies,
        avg_triage_time_minutes=2.5,
        severity_distribution=severity_dist,
        care_level_distribution=care_dist,
        top_complaints=top_complaints,
        provider_utilization=provider_util,
        hourly_case_volume=hourly_volume,
        triage_accuracy_rate=round(accuracy_rate, 1),
    )
