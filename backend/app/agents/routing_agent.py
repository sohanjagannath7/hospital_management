from typing import Optional, Dict, Any
from app.agents.base_agent import call_gemini

SYSTEM = """You are a healthcare patient routing AI. Based on triage severity and clinical assessment,
route the patient to the most appropriate care setting. Return your decision as JSON."""

SCHEMA = {
    "type": "object",
    "properties": {
        "care_level": {
            "type": "string",
            "enum": ["Emergency Room", "Urgent Care", "Primary Care", "Telehealth", "Mental Health", "Specialist", "Self Care"]
        },
        "reasoning": {"type": "string"},
        "specialty_needed": {"type": "string"},
        "time_sensitivity": {
            "type": "string",
            "enum": ["immediate", "within_1_hour", "within_4_hours", "within_24_hours", "within_48_hours", "routine"]
        },
        "alternative_care_levels": {"type": "array", "items": {"type": "string"}},
        "transport_recommendation": {"type": "string"},
    },
    "required": ["care_level", "reasoning", "time_sensitivity"]
}

CARE_GUIDE = (
    "Emergency Room: ESI-1/2 or life-threatening. "
    "Urgent Care: ESI-3, same-day non-life-threatening. "
    "Primary Care: ESI-4/5, within 24-48h. "
    "Telehealth: Non-urgent, can be assessed remotely. "
    "Mental Health: Psychiatric conditions. "
    "Specialist: Needs specialty consultation. "
    "Self Care: Minor, home treatment sufficient."
)


def route_patient(
    severity: Optional[str],
    symptom_analysis: Dict[str, Any],
    vital_signs: Optional[Dict],
    medical_history: Optional[Dict],
) -> Dict[str, Any]:
    info = (
        f"ESI Level: {severity or 'Unknown'}\n"
        f"Possible Conditions: {', '.join(symptom_analysis.get('possible_conditions', [])[:5])}\n"
        f"Red Flags: {', '.join(symptom_analysis.get('red_flags', []))}\n"
        f"Body Systems: {', '.join(symptom_analysis.get('body_systems_affected', []))}\n"
        f"Risk Factors: {', '.join(symptom_analysis.get('risk_factors', []))}\n"
        f"\nCare Level Guide: {CARE_GUIDE}\n"
    )
    if medical_history and medical_history.get("chronic_conditions"):
        info += f"Chronic Conditions: {', '.join(medical_history['chronic_conditions'])}\n"

    result, _ = call_gemini(
        system=SYSTEM,
        user_message=f"Route this patient to appropriate care:\n{info}",
        json_schema=SCHEMA,
    )

    default_map = {
        "ESI-1": "Emergency Room", "ESI-2": "Emergency Room",
        "ESI-3": "Urgent Care", "ESI-4": "Primary Care", "ESI-5": "Self Care",
    }
    return result or {
        "care_level": default_map.get(severity, "Urgent Care"),
        "reasoning": "Default routing based on severity level",
        "time_sensitivity": "within_4_hours",
    }
