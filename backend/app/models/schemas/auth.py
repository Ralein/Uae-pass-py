from pydantic import BaseModel, Field

class OTPRequest(BaseModel):
    identifier: str = Field(..., description="National ID, Email, or Phone")

class OTPVerify(BaseModel):
    request_id: str
    otp: str = Field(..., min_length=6, max_length=6)

class PINSet(BaseModel):
    pin: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
