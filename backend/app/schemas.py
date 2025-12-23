# app/schemas.py
from pydantic import BaseModel, EmailStr

class LeadCreate(BaseModel):
    business_name: str
    email: EmailStr
    industry: str
    city: str

class LeadResponse(BaseModel):
    id: int
    business_name: str
    email: str
    industry: str
    city: str
    status: str

    class Config:
        orm_mode = True


class AIEmailResponse(BaseModel):
    subject: str
    body: str


class OutreachResponse(BaseModel):
    message: str
    lead_status: str
