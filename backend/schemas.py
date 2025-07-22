# backend/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

# ====================
# User Schemas
# ====================

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True # Assuming all registered users are active by default

    class Config:
        from_attributes = True # Pydantic v2 replaces orm_mode

# ====================
# Token Schemas
# ====================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

# ====================
# Analysis Schemas
# ====================

class AnalysisBase(BaseModel):
    job_description: str
    resume_filename: str
    analysis_result: dict

# This is the main schema that will be returned by the API endpoint.
# It includes all data from the database model for a single analysis.
class Analysis(AnalysisBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True