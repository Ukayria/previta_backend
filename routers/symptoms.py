from fastapi import APIRouter, HTTPException
from models.schemas import SymptomCheckRequest, SymptomCheckResponse
from services.llm import analyze_with_llm, get_chat_system_prompt
from services.risk_engine import apply_risk_rules
from pydantic import BaseModel
from typing import List
import uuid
import os
import requests as req
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["symptoms"])


# ─── Symptom Check ─────────────────────────────────────────────
@router.post("/symptom-check", response_model=SymptomCheckResponse)
async def symptom_check(request: SymptomCheckRequest):
    try:
        payload = request.model_dump()

        # 1. Get LLM analysis
        llm_result = await analyze_with_llm(payload)

        # 2. Apply deterministic safety rules
        final_result = apply_risk_rules(llm_result, payload["symptoms"], payload["severity"])

        # 3. Add metadata
        final_result["check_id"] = str(uuid.uuid4())
        final_result["created_at"] = datetime.utcnow()

        # 4. TODO: Save to Supabase here

        return final_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Chat ──────────────────────────────────────────────────────
class ChatMessageItem(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessageItem]
    language: str = "English"

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        language = request.language
        system_prompt = get_chat_system_prompt(language)

        messages = [{"role": m.role, "content": m.content} for m in request.messages]

        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "temperature": 0.7,
            "max_tokens": 200
        }

        response = req.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body
        )
        response.raise_for_status()

        reply = response.json()["choices"][0]["message"]["content"]
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))