from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models import UserRole, SeverityLevel, CaseStatus, CareLevel, ProviderStatus


# ─── Auth ──────────────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str
    user: "UserOut"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.patient
    phone: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    phone: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ─── Patient ───────────────────────────────────────────────────────────────────

class MedicalHistoryCreate(BaseModel):
    chronic_conditions: List[str] = []
    past_surgeries: List[str] = []
    allergies: List[str] = []
    current_medications: List[Dict[str, str]] = []
    family_history: List[str] = []
    immunizations: List[str] = []
    smoking_status: Optional[str] = None
    alcohol_use: Optional[str] = None
    exercise_frequency: Optional[str] = None


class MedicalHistoryOut(MedicalHistoryCreate):
    id: int
    patient_id: int
    updated_at: datetime

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None
    blood_type: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_id: Optional[str] = None
    address: Optional[str] = None


class PatientOut(PatientCreate):
    id: int
    user_id: int
    user: UserOut
    medical_history: Optional[MedicalHistoryOut] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Provider ──────────────────────────────────────────────────────────────────

class ProviderCreate(BaseModel):
    specialty: str
    department: Optional[str] = None
    license_number: Optional[str] = None
    years_experience: Optional[int] = None
    max_cases: int = 10
    available_care_levels: List[str] = []


class ProviderOut(ProviderCreate):
    id: int
    user_id: int
    status: ProviderStatus
    current_load: int
    rating: float
    user: UserOut
    created_at: datetime

    class Config:
        from_attributes = True


class ProviderStatusUpdate(BaseModel):
    status: ProviderStatus


# ─── Triage Case ───────────────────────────────────────────────────────────────

class VitalSigns(BaseModel):
    temperature_c: Optional[float] = None
    heart_rate: Optional[int] = None
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    oxygen_saturation: Optional[float] = None
    respiratory_rate: Optional[int] = None
    glucose_mg_dl: Optional[float] = None


class TriageCaseCreate(BaseModel):
    chief_complaint: str
    symptoms: List[str]
    symptom_duration: Optional[str] = None
    pain_scale: Optional[int] = None
    vital_signs: Optional[VitalSigns] = None
    onset_description: Optional[str] = None

    @field_validator("pain_scale")
    @classmethod
    def validate_pain_scale(cls, v):
        if v is not None and not (0 <= v <= 10):
            raise ValueError("Pain scale must be between 0 and 10")
        return v


class TriageAssessmentOut(BaseModel):
    id: int
    symptom_analysis: Optional[Dict[str, Any]]
    possible_conditions: List[str]
    severity_reasoning: Optional[str]
    risk_factors: List[str]
    drug_interactions: List[Dict[str, Any]]
    routing_reasoning: Optional[str]
    confidence_score: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class RecommendationOut(BaseModel):
    id: int
    recommendation_type: str
    title: str
    description: str
    priority: str
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CaseAssignmentOut(BaseModel):
    id: int
    provider_id: int
    provider: ProviderOut
    assigned_at: datetime
    accepted_at: Optional[datetime]
    notes: Optional[str]

    class Config:
        from_attributes = True


class TriageCaseOut(BaseModel):
    id: int
    case_number: str
    patient_id: int
    chief_complaint: str
    symptoms: List[str]
    symptom_duration: Optional[str]
    pain_scale: Optional[int]
    vital_signs: Optional[Dict[str, Any]]
    onset_description: Optional[str]
    status: CaseStatus
    severity: Optional[SeverityLevel]
    care_level: Optional[CareLevel]
    is_emergency: bool
    created_at: datetime
    updated_at: Optional[datetime]
    assessment: Optional[TriageAssessmentOut] = None
    recommendations: List[RecommendationOut] = []
    assignment: Optional[CaseAssignmentOut] = None

    class Config:
        from_attributes = True


class CaseOutcomeCreate(BaseModel):
    final_diagnosis: str
    treatment_provided: str
    outcome_status: str
    triage_accuracy: Optional[bool] = None
    provider_notes: Optional[str] = None
    follow_up_required: bool = False
    follow_up_date: Optional[datetime] = None


# ─── Chat ──────────────────────────────────────────────────────────────────────

class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionOut(BaseModel):
    id: int
    is_active: bool
    messages: List[ChatMessageOut] = []
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Analytics ─────────────────────────────────────────────────────────────────

class AnalyticsSummary(BaseModel):
    total_cases: int
    pending_cases: int
    active_cases: int
    completed_cases: int
    emergency_cases: int
    avg_triage_time_minutes: float
    severity_distribution: Dict[str, int]
    care_level_distribution: Dict[str, int]
    top_complaints: List[Dict[str, Any]]
    provider_utilization: List[Dict[str, Any]]
    hourly_case_volume: List[Dict[str, Any]]
    triage_accuracy_rate: float


# ─── Alert ─────────────────────────────────────────────────────────────────────

class AlertOut(BaseModel):
    id: int
    case_id: int
    alert_type: str
    message: str
    is_acknowledged: bool
    created_at: datetime

    class Config:
        from_attributes = True
