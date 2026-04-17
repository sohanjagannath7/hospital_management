"""
Triage Orchestrator: coordinates all sub-agents to produce a full triage assessment.
Pipeline: symptom_analyzer → severity_scorer → routing_agent → recommendation_agent → drug_interaction_agent
"""
import json
import time
from typing import Dict, Any, Optional
from app.agents.symptom_analyzer import analyze_symptoms
from app.agents.severity_scorer import score_severity
from app.agents.routing_agent import route_patient
from app.agents.recommendation_agent import generate_recommendations
from app.agents.drug_interaction_agent import check_drug_interactions


async def run_triage(
    chief_complaint: str,
    symptoms: list,
    symptom_duration: Optional[str],
    pain_scale: Optional[int],
    vital_signs: Optional[Dict],
    onset_description: Optional[str],
    medical_history: Optional[Dict],
) -> Dict[str, Any]:
    """
    Runs the full agentic triage pipeline.
    Returns a structured assessment dict.
    """
    start = time.time()

    # Step 1: Analyze symptoms
    symptom_result = analyze_symptoms(
        chief_complaint=chief_complaint,
        symptoms=symptoms,
        duration=symptom_duration,
        pain_scale=pain_scale,
        onset=onset_description,
        vitals=vital_signs,
        history=medical_history,
    )

    # Step 2: Score severity (ESI 1-5)
    severity_result = score_severity(
        symptom_analysis=symptom_result,
        vital_signs=vital_signs,
        pain_scale=pain_scale,
        medical_history=medical_history,
    )

    # Step 3: Check drug interactions (if patient has medications)
    current_meds = []
    if medical_history and medical_history.get("current_medications"):
        current_meds = [m.get("name", m) if isinstance(m, dict) else m
                        for m in medical_history["current_medications"]]
    drug_result = check_drug_interactions(
        symptoms=symptoms,
        possible_conditions=symptom_result.get("possible_conditions", []),
        current_medications=current_meds,
    )

    # Step 4: Route patient to appropriate care
    routing_result = route_patient(
        severity=severity_result.get("esi_level"),
        symptom_analysis=symptom_result,
        vital_signs=vital_signs,
        medical_history=medical_history,
    )

    # Step 5: Generate recommendations
    recommendation_result = generate_recommendations(
        chief_complaint=chief_complaint,
        symptom_analysis=symptom_result,
        severity=severity_result.get("esi_level"),
        care_level=routing_result.get("care_level"),
        drug_interactions=drug_result.get("interactions", []),
    )

    total_ms = int((time.time() - start) * 1000)

    is_emergency = severity_result.get("esi_level") in ("ESI-1", "ESI-2")

    return {
        "symptom_analysis": symptom_result,
        "possible_conditions": symptom_result.get("possible_conditions", []),
        "severity": severity_result.get("esi_level", "ESI-3"),
        "severity_reasoning": severity_result.get("reasoning", ""),
        "risk_factors": symptom_result.get("risk_factors", []),
        "care_level": routing_result.get("care_level", "Urgent Care"),
        "routing_reasoning": routing_result.get("reasoning", ""),
        "recommendations": recommendation_result.get("recommendations", []),
        "drug_interactions": drug_result.get("interactions", []),
        "is_emergency": is_emergency,
        "confidence_score": severity_result.get("confidence", 0.8),
        "processing_time_ms": total_ms,
    }
