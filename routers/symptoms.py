# routers/symptoms.py
from fastapi import APIRouter, HTTPException
from models.schemas import SymptomCheckRequest, SymptomCheckResponse
from services.llm import analyze_with_llm
from services.risk_engine import apply_risk_rules
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/v1", tags=["symptoms"])

@router.post("/symptom-check", response_model=SymptomCheckResponse)
async def symptom_check(request: SymptomCheckRequest):
    try:
        payload = request.model_dump()
        
        # 1. Get LLM analysis
        llm_result = await analyze_with_llm(payload)
        
        # 2. Apply your deterministic safety rules
        final_result = apply_risk_rules(llm_result, payload["symptoms"], payload["severity"])
        
        # 3. Add metadata
        final_result["check_id"] = str(uuid.uuid4())
        final_result["created_at"] = datetime.utcnow()
        
        # 4. TODO: Save to Supabase here
        
        return final_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))