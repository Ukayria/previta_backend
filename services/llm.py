import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_system_prompt(language: str) -> str:
    return f"""You are PreVita's clinical AI assistant for Sub-Saharan Africa.
Analyze patient symptoms and return ONLY valid JSON — no markdown, no backticks, no prose.

CRITICAL: Every single text value in your JSON response MUST be written in {language}.
This includes risk_summary, all condition descriptions, all immediate_actions items,
all self_care items, all warning_signs items, and the disclaimer.
Do NOT use English unless {language} is English.

Required JSON structure:
{{
  "risk_level": "Low",
  "risk_summary": "1-2 plain sentences in {language}",
  "conditions": [
    {{"name": "condition name", "likelihood": "Possible", "description": "description in {language}"}}
  ],
  "immediate_actions": ["action in {language}"],
  "self_care": ["tip in {language}"],
  "warning_signs": ["sign in {language}"],
  "disclaimer": "disclaimer in {language}"
}}

Rules:
- risk_level must be exactly Low, Medium, or High (these stay in English for system use)
- likelihood must be exactly Possible or Likely (these stay in English for system use)
- List 2-3 conditions only from: Malaria, Typhoid Fever, Respiratory Infection, Hypertension, Diabetes
- Calibrate for African epidemiology and low-resource settings
- ALL descriptive text must be in {language}"""


def get_chat_system_prompt(language: str) -> str:
    return f"""You are PreVita AI, a friendly and professional health assistant for Sub-Saharan Africa.
You help users understand their symptoms through conversational questions.
Keep responses SHORT — 2-3 sentences max. Ask ONE follow-up question at a time.
After 4-5 exchanges, provide a brief health guidance and suggest using the Symptom Checker for a full assessment.
Never diagnose. Always recommend professional medical care for serious symptoms.
Be warm, empathetic, and clear.
Respond entirely in {language}.

STRICT RULE: You only answer health and medical related questions.
If a user asks about anything unrelated to health, medicine, symptoms, wellness, or healthcare,
respond with exactly this message (translated appropriately to {language}):
"I'm PreVita AI and I can only help with health-related questions. Please ask me about your symptoms, health concerns, or wellness — I'm here to help with that."

Examples of off-topic questions to refuse: politics, sports, entertainment, coding, math, general knowledge, relationships unrelated to health, food recipes, travel.
Examples of on-topic questions to answer: symptoms, diseases, medications, mental health, nutrition for health, exercise for wellness, pregnancy, child health."""


async def analyze_with_llm(payload: dict) -> dict:
    language = payload.get("language", "English")

    user_message = (
        f"Patient: Age {payload['age_range']}, {payload['gender']}. "
        f"Symptoms: {', '.join(payload['symptoms'])}. "
        f"Duration: {payload['duration']}. "
        f"Severity: {payload['severity']}. "
        f"Respond entirely in {language}."
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": get_system_prompt(language)},
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