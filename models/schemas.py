from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime

class SymptomCheckRequest(BaseModel):
    user_id: str
    age_range: str
    gender: str
    symptoms: List[str]
    duration: str
    severity: Literal["Mild", "Moderate", "Severe"]
    language: str = "English"

class Condition(BaseModel):
    name: str
    likelihood: Literal["Possible", "Likely"]
    description: str

class SymptomCheckResponse(BaseModel):
    check_id: str
    risk_level: Literal["Low", "Medium", "High"]
    risk_summary: str
    conditions: List[Condition]
    immediate_actions: List[str]
    self_care: List[str]
    warning_signs: List[str]
    disclaimer: str
    created_at: datetime