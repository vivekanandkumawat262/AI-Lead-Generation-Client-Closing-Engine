from ..dependencies.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import EmailLog, Lead, Message
from ..schemas import AIEmailResponse
from app.services.ai_email_service import generate_ai_email

router = APIRouter(prefix="/ai", tags=["AI"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/email", response_model=AIEmailResponse)
def generate_email(lead_id: int, db: Session = Depends(get_db),
    user=Depends(get_current_user)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    email_data = generate_ai_email(lead)
     # 🔹 Save to EmailLog
    email_log = EmailLog(
        lead_id=lead.id,
        subject=email_data["subject"],
        body=email_data["body"]
    )

    message_log = Message(
        lead_id=lead.id,
        subject=email_data["subject"],
        content=email_data["body"]
    )
    
    db.add(message_log)
    db.add(email_log)
    db.commit()
    db.refresh(email_log)

    return email_data
