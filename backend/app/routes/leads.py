# app/routes/leads.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Lead, LeadStatus
from ..schemas import LeadCreate, LeadResponse
from ..dependencies.auth import get_current_user
from app.dependencies.roles import require_role
from app.core.roles import Role



router = APIRouter(prefix="/leads", tags=["Leads"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=LeadResponse)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role([Role.ADMIN, Role.AGENT]))   # 🔐 JWT PROTECTION
):
    existing = db.query(Lead).filter(Lead.email == lead.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Lead already exists")

    new_lead = Lead(
        business_name=lead.business_name,
        email=lead.email,
        industry=lead.industry,
        city=lead.city,
        status=LeadStatus.NEW.value
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead


@router.get("/", response_model=list[LeadResponse])
def list_leads(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)   # 🔐 JWT PROTECTION
):
    return db.query(Lead).all()
