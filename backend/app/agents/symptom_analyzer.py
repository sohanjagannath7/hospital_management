from typing import Optional, Dict, Any, List
from app.agents.base_agent import call_gemini

SYSTEM = """You are a clinical symptom analysis AI. Analyze patient symptoms and return a structured medical assessment as JSON."""

SCHEMA = {
    "type": "object",
    "properties": {
        "possible_conditions": {"type": "array", "items": {"type": "string"}},
        "risk_factors": {"type": "array", "items": {"type": "string"}},
        "red_flags": {"type": "array", "items": {"type": "string"}},
        "body_systems_affected": {"type": "array", "items": {"type": "string"}},
        "urgency_indicators": {"type": "array", "items": {"type": "string"}},
        "clinical_summary": {"type": "string"},
    },
    "required": ["possible_conditions", "risk_factors", "red_flags", "clinical_summary"]
}


def analyze_symptoms(
    chief_complaint: str,
    symptoms: List[str],
    duration: Optional[str],
    pain_scale: Optional[int],
    onset: Optional[str],
    vitals: Optional[Dict],
    history: Optional[Dict],
) -> Dict[str, Any]:
    patient_info = (
        f"Chief Complaint: {chief_complaint}\n"
        f"Symptoms: {', '.join(symptoms)}\n"
        f"Duration: {duration or 'Not specified'}\n"
        f"Pain Scale: {f'{pain_scale}/10' if pain_scale is not None else 'Not reported'}\n"
        f"Onset: {onset or 'Not specified'}\n"
    )

    if vitals:
        lines = [f"  {k}: {v}" for k, v in vitals.items() if v is not None]
        if lines:
            patient_info += "Vital Signs:\n" + "\n".join(lines) + "\n"

    if history:
        if history.get("chronic_conditions"):
            patient_info += f"Chronic Conditions: {', '.join(history['chronic_conditions'])}\n"
        if history.get("allergies"):
            patient_info += f"Allergies: {', '.join(history['allergies'])}\n"
        if history.get("current_medications"):
            meds = [m.get("name", str(m)) if isinstance(m, dict) else str(m) for m in history["current_medications"]]
            patient_info += f"Current Medications: {', '.join(meds)}\n"

    result, _ = call_gemini(
        system=SYSTEM,
        user_message=f"Analyze this patient presentation:\n{patient_info}",
        json_schema=SCHEMA,
    )

    return result or {
        "possible_conditions": ["Undetermined — manual review required"],
        "risk_factors": [],
        "red_flags": [],
        "clinical_summary": chief_complaint,
    }
