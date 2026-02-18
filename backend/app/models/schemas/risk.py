from enum import Enum
from pydantic import BaseModel
from typing import Optional

class RiskAction(str, Enum):
    ALLOW = "allow"
    STEP_UP = "step_up"
    BLOCK = "block"

class AuthContext(BaseModel):
    ip_address: str
    user_agent: str
    fingerprint: str
    user_id: Optional[str] = None

class RiskScore(BaseModel):
    total_score: int
    action: RiskAction
    factors: list[str] = []
