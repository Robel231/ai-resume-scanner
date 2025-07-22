

from pydantic import BaseModel, EmailStr
from datetime import datetime





class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool = True 

    class Config:
        from_attributes = True 





class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None





class AnalysisBase(BaseModel):
    job_description: str
    resume_filename: str
    analysis_result: dict



class Analysis(AnalysisBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True