from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class UserCreate(BaseModel):
    national_id: str = Field(..., description="UAE National ID format 784-XXXX-XXXXXXX-X")
    email: EmailStr
    phone: str = Field(..., pattern=r"^\+9715\d{8}$")
    full_name: str

    @field_validator("national_id")
    @classmethod
    def validate_national_id(cls, v: str) -> str:
        # Simple regex for format validation
        if not re.match(r"^784-\d{4}-\d{7}-\d{1}$", v):
            raise ValueError("Invalid National ID format")
        return v

class UserResponse(BaseModel):
    id: str
    is_active: bool
    # We generally don't return PII unless specifically requested/authorized
    # For this schema, we returning masked versions could be a good practice, 
    # but for now keeping it minimal.
