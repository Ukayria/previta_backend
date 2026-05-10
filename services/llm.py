import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """You are PreVita's clinical AI assistant for Sub-Saharan Africa.
Analyze patient symptoms and return ONLY valid JSON — no markdown, no backticks, no prose.

Required JSON structure:
{
  "risk_level": "Low",
  "risk_summary": "1-2 plain sentences",
  "conditions": [
    {"name": "...", "likelihood": "Possible", "description": "..."}
  ],
  "immediate_actions": ["..."],
  "self_care": ["..."],
  "warning_signs": ["..."],
  "disclaimer": "..."
}

Rules:
- risk_level must be exactly Low, Medium, or High
- likelihood must be exactly Possible or Likely
- List 2-3 conditions only from: Malaria, Typhoid Fever, Respiratory Infection, Hypertension, Diabetes
- Calibrate for African epidemiology and low-resource settings
- Always include a medical disclaimer"""


async def analyze_with_llm(payload: dict) -> dict:
    user_message = (
        f"Patient: Age {payload['age_range']}, {payload['gender']}. "
        f"Symptoms: {', '.join(payload['symptoms'])}. "
        f"Duration: {payload['duration']}. "
        f"Severity: {payload['severity']}."
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.2,
        "max_tokens": 1024
    }

    response = requests.post(GROQ_URL, headers=headers, json=body)
    response.raise_for_status()

    text = response.json()["choices"][0]["message"]["content"].strip()

    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    return json.loads(text.strip())