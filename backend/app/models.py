from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey,
    Enum as SQLEnum, JSON, ARRAY
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    patient = "patient"
    doctor = "doctor"
    nurse = "nurse"
    admin = "admin"


class SeverityLevel(str, enum.Enum):
    esi_1 = "ESI-1"   # Resuscitation - Immediate life threat
    esi_2 = "ESI-2"   # Emergent - High risk
    esi_3 = "ESI-3"   # Urgent - Multiple resources needed
    esi_4 = "ESI-4"   # Less Urgent - One resource needed
    esi_5 = "ESI-5"   # Non-Urgent - No resources needed


class CaseStatus(str, enum.Enum):
    pending = "pending"
    triaging = "triaging"
    triaged = "triaged"
    assigned = "assigned"
    in_progress = "in_progress"
    completed = "completed"
    escalated = "escalated"
    cancelled = "cancelled"


class CareLevel(str, enum.Enum):
    emergency = "Emergency Room"
    urgent_care = "Urgent Care"
    primary_care = "Primary Care"
    telehealth = "Telehealth"
    self_care = "Self Care"
    mental_health = "Mental Health"
    specialist = "Specialist"


class ProviderStatus(str, enum.Enum):
    available = "available"
    busy = "busy"
    offline = "offline"
    on_break = "on_break"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.patient, nullable=False)
    is_active = Column(Boolean, default=True)
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    patient = relationship("Patient", back_populates="user", uselist=False)
    provider = relationship("Provider", back_populates="user", uselist=False)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    date_of_birth = Column(DateTime)
    gender = Column(String(20))
    blood_type = Column(String(10))
    height_cm = Column(Float)
    weight_kg = Column(Float)
    emergency_contact_name = Column(String(255))
    emergency_contact_phone = Column(String(20))
    insurance_provider = Column(String(255))
    insurance_id = Column(String(100))
    address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="patient")
    medical_history = relationship("MedicalHistory", back_populates="patient", uselist=False)
    triage_cases = relationship("TriageCase", back_populates="patient")
    chat_sessions = relationship("ChatSession", back_populates="patient")


class MedicalHistory(Base):
    __tablename__ = "medical_histories"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), unique=True)
    chronic_conditions = Column(JSON, default=list)
    past_surgeries = Column(JSON, default=list)
    allergies = Column(JSON, default=list)
    current_medications = Column(JSON, default=list)
    family_history = Column(JSON, default=list)
    immunizations = Column(JSON, default=list)
    smoking_status = Column(String(50))
    alcohol_use = Column(String(50))
    exercise_frequency = Column(String(50))
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    patient = relationship("Patient", back_populates="medical_history")


class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    specialty = Column(String(255), nullable=False)
    department = Column(String(255))
    license_number = Column(String(100))
    years_experience = Column(Integer)
    status = Column(SQLEnum(ProviderStatus), default=ProviderStatus.available)
    max_cases = Column(Integer, default=10)
    current_load = Column(Integer, default=0)
    available_care_levels = Column(JSON, default=list)
    rating = Column(Float, default=5.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="provider")
    case_assignments = relationship("CaseAssignment", back_populates="provider")


class TriageCase(Base):
    __tablename__ = "triage_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(20), unique=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    chief_complaint = Column(Text, nullable=False)
    symptoms = Column(JSON, default=list)
    symptom_duration = Column(String(100))
    pain_scale = Column(Integer)
    vital_signs = Column(JSON, default=dict)
    onset_description = Column(Text)
    status = Column(SQLEnum(CaseStatus), default=CaseStatus.pending)
    severity = Column(SQLEnum(SeverityLevel))
    care_level = Column(SQLEnum(CareLevel))
    is_emergency = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

    patient = relationship("Patient", back_populates="triage_cases")
    assessment = relationship("TriageAssessment", back_populates="case", uselist=False)
    assignment = relationship("CaseAssignment", back_populates="case", uselist=False)
    recommendations = relationship("Recommendation", back_populates="case")
    outcome = relationship("CaseOutcome", back_populates="case", uselist=False)
    alerts = relationship("Alert", back_populates="case")


class TriageAssessment(Base):
    __tablename__ = "triage_assessments"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("triage_cases.id"), unique=True)
    symptom_analysis = Column(JSON)
    possible_conditions = Column(JSON, default=list)
    severity_reasoning = Column(Text)
    risk_factors = Column(JSON, default=list)
    drug_interactions = Column(JSON, default=list)
    routing_reasoning = Column(Text)
    confidence_score = Column(Float)
    agent_version = Column(String(50))
    processing_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    case = relationship("TriageCase", back_populates="assessment")


class CaseAssignment(Base):
    __tablename__ = "case_assignments"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("triage_cases.id"), unique=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    accepted_at = Column(DateTime(timezone=True))
    notes = Column(Text)

    case = relationship("TriageCase", back_populates="assignment")
    provider = relationship("Provider", back_populates="case_assignments")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("triage_cases.id"))
    recommendation_type = Column(String(50))  # test, consultation, medication, self-care
    title = Column(String(255))
    description = Column(Text)
    priority = Column(String(20))  # urgent, high, medium, low
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    case = relationship("TriageCase", back_populates="recommendations")


class CaseOutcome(Base):
    __tablename__ = "case_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("triage_cases.id"), unique=True)
    final_diagnosis = Column(Text)
    treatment_provided = Column(Text)
    outcome_status = Column(String(50))  # improved, stable, deteriorated, referred
    triage_accuracy = Column(Boolean)
    provider_notes = Column(Text)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    case = relationship("TriageCase", back_populates="outcome")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("triage_cases.id"))
    alert_type = Column(String(50))  # emergency, drug_interaction, deterioration, overdue
    message = Column(Text)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    case = relationship("TriageCase", back_populates="alerts")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String(20))  # user, assistant
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ChatSession", back_populates="messages")
