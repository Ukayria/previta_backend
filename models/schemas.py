# models/schemas.py
from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime

class SymptomCheckRequest(BaseModel):
    user_id: str
    age_range: str          # "18-30", "31-45", etc.
    gender: str
    symptoms: List[str]     # ["Fever", "Headache", "Chills"]
    duration: str           # "2-3 days"
    severity: Literal["Mild", "Moderate", "Severe"]

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