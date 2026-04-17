from typing import Dict, Any, List
from app.agents.base_agent import call_gemini

SYSTEM = """You are a clinical pharmacology AI. Check for drug-drug interactions and contraindications.
Return your findings as JSON. If no medications are provided, return empty interactions."""

SCHEMA = {
    "type": "object",
    "properties": {
        "interactions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "drugs_involved": {"type": "array", "items": {"type": "string"}},
                    "severity": {"type": "string", "enum": ["contraindicated", "major", "moderate", "minor"]},
                    "description": {"type": "string"},
                    "recommendation": {"type": "string"},
                },
                "required": ["severity", "description", "recommendation"]
            }
        },
        "allergy_alerts": {"type": "array", "items": {"type": "string"}},
        "safe_to_proceed": {"type": "boolean"},
    },
    "required": ["interactions", "safe_to_proceed"]
}


def check_drug_interactions(
    symptoms: List[str],
    possible_conditions: List[str],
    current_medications: List[str],
) -> Dict[str, Any]:
    if not current_medications:
        return {"interactions": [], "safe_to_proceed": True, "allergy_alerts": []}

    info = (
        f"Current Medications: {', '.join(current_medications)}\n"
        f"Presenting Conditions: {', '.join(possible_conditions[:5])}\n"
        f"Symptoms: {', '.join(symptoms[:10])}\n"
        "Check for: drug-drug interactions, contraindications, medications masking symptoms."
    )

    result, _ = call_gemini(system=SYSTEM, user_message=info, json_schema=SCHEMA)
    return result or {"interactions": [], "safe_to_proceed": True, "allergy_alerts": []}
