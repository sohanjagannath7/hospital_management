from typing import Optional, Dict, Any
from app.agents.base_agent import call_gemini

SYSTEM = """You are an emergency triage severity scoring AI using the Emergency Severity Index (ESI) 5-level system.
ESI-1: Immediate life threat. ESI-2: High risk/emergent. ESI-3: Urgent, needs resources.
ESI-4: Less urgent. ESI-5: Non-urgent. Return your assessment as JSON."""

SCHEMA = {
    "type": "object",
    "properties": {
        "esi_level": {"type": "string", "enum": ["ESI-1", "ESI-2", "ESI-3", "ESI-4", "ESI-5"]},
        "reasoning": {"type": "string"},
        "confidence": {"type": "number"},
        "vital_sign_concerns": {"type": "array", "items": {"type": "string"}},
        "immediate_actions": {"type": "array", "items": {"type": "string"}},
        "expected_wait_minutes": {"type": "integer"},
    },
    "required": ["esi_level", "reasoning", "confidence"]
}


def score_severity(
    symptom_analysis: Dict[str, Any],
    vital_signs: Optional[Dict],
    pain_scale: Optional[int],
    medical_history: Optional[Dict],
) -> Dict[str, Any]:
    red_flags = symptom_analysis.get("red_flags", [])
    conditions = symptom_analysis.get("possible_conditions", [])
    risk_factors = symptom_analysis.get("risk_factors", [])

    info = (
        f"Possible Conditions: {', '.join(conditions[:5])}\n"
        f"Red Flags: {', '.join(red_flags)}\n"
        f"Risk Factors: {', '.join(risk_factors)}\n"
        f"Pain Scale: {f'{pain_scale}/10' if pain_scale is not None else 'Not reported'}\n"
    )

    if vital_signs:
        abnormal = []
        hr = vital_signs.get("heart_rate")
        o2 = vital_signs.get("oxygen_saturation")
        sbp = vital_signs.get("blood_pressure_systolic")
        temp = vital_signs.get("temperature_c")
        rr = vital_signs.get("respiratory_rate")
        if hr and (hr < 50 or hr > 120): abnormal.append(f"HR {hr} bpm")
        if o2 and o2 < 94: abnormal.append(f"O2 sat {o2}%")
        if sbp and (sbp < 90 or sbp > 180): abnormal.append(f"SBP {sbp} mmHg")
        if temp and (temp < 35 or temp > 38.5): abnormal.append(f"Temp {temp}°C")
        if rr and (rr < 12 or rr > 25): abnormal.append(f"RR {rr}/min")
        if abnormal:
            info += f"Abnormal Vitals: {', '.join(abnormal)}\n"

    if medical_history and medical_history.get("chronic_conditions"):
        info += f"Chronic Conditions: {', '.join(medical_history['chronic_conditions'])}\n"

    result, _ = call_gemini(
        system=SYSTEM,
        user_message=f"Assign ESI triage level for this patient:\n{info}",
        json_schema=SCHEMA,
    )

    return result or {"esi_level": "ESI-3", "reasoning": "Default — manual review recommended", "confidence": 0.5}
