# services/risk_engine.py

HIGH_RISK_SYMPTOMS = {"Difficulty breathing", "Chest pain / palpitations", "Rapid heartbeat"}
HIGH_RISK_SYMPTOM_COUNT = 5   # 5+ symptoms always = at least Medium

def apply_risk_rules(llm_result: dict, symptoms: list, severity: str) -> dict:
    """Override or escalate LLM risk based on deterministic rules."""
    
    current_risk = llm_result.get("risk_level", "Low")
    
    # Rule 1: Any high-risk symptom present → minimum Medium
    if any(s in HIGH_RISK_SYMPTOMS for s in symptoms):
        if current_risk == "Low":
            llm_result["risk_level"] = "Medium"
            llm_result["risk_summary"] += " Some of your symptoms require prompt attention."
    
    # Rule 2: Severe + 3+ symptoms → minimum High
    if severity == "Severe" and len(symptoms) >= 3:
        llm_result["risk_level"] = "High"
    
    # Rule 3: Breathing difficulty is always High
    if "Difficulty breathing" in symptoms:
        llm_result["risk_level"] = "High"
    
    return llm_result