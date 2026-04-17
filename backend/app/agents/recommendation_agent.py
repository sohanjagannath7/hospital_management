from typing import Dict, Any, List, Optional
from app.agents.base_agent import call_gemini

SYSTEM = """You are a clinical recommendation AI. Generate specific, actionable clinical recommendations
for diagnostic tests, specialist consultations, medications, and next steps. Return as JSON."""

SCHEMA = {
    "type": "object",
    "properties": {
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["diagnostic_test", "consultation", "medication", "self_care", "monitoring", "follow_up"]},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["urgent", "high", "medium", "low"]},
                    "rationale": {"type": "string"},
                },
                "required": ["type", "title", "description", "priority"]
            }
        },
        "patient_instructions": {"type": "string"},
        "warning_signs": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["recommendations", "patient_instructions"]
}


def generate_recommendations(
    chief_complaint: str,
    symptom_analysis: Dict[str, Any],
    severity: Optional[str],
    care_level: Optional[str],
    drug_interactions: List[Dict],
) -> Dict[str, Any]:
    interactions_text = ""
    if drug_interactions:
        lines = [f"  - {i.get('description', str(i))}" for i in drug_interactions[:3]]
        interactions_text = "\nDrug Interactions Detected:\n" + "\n".join(lines)

    info = (
        f"Chief Complaint: {chief_complaint}\n"
        f"ESI Level: {severity}\n"
        f"Assigned Care Level: {care_level}\n"
        f"Possible Conditions: {', '.join(symptom_analysis.get('possible_conditions', [])[:5])}\n"
        f"Red Flags: {', '.join(symptom_analysis.get('red_flags', []))}\n"
        f"Body Systems: {', '.join(symptom_analysis.get('body_systems_affected', []))}\n"
        f"{interactions_text}\n"
        "Generate recommendations including: diagnostic tests, specialist consultations, medications, self-care, follow-up."
    )

    result, _ = call_gemini(system=SYSTEM, user_message=info, json_schema=SCHEMA)

    return result or {
        "recommendations": [{"type": "consultation", "title": "Medical Evaluation", "description": "Schedule appointment with a healthcare provider.", "priority": "high"}],
        "patient_instructions": "Please seek medical attention as directed.",
    }
