from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import SessionLocal
from ..models import Lead, LeadStatus, Message, EmailLog
from ..schemas import OutreachResponse

router = APIRouter(prefix="/outreach", tags=["Outreach"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send", response_model=OutreachResponse)
def send_email(lead_id: int, db: Session = Depends(get_db)):
    # 1. Fetch lead
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # 2. Enforce status rule
    if lead.status != LeadStatus.NEW.value:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot send email when lead status is {lead.status}"
        )

    # 3. Get latest AI-generated message
    message = (
        db.query(Message)
        .filter(Message.lead_id == lead.id)
        .order_by(Message.created_at.desc())
        .first()
    )

    if not message:
        raise HTTPException(
            status_code=400,
            detail="No AI-generated email found for this lead"
        )

    # 4. MOCK EMAIL SEND (replace with SMTP later)
    print("=== SENDING EMAIL ===")
    print(f"To: {lead.email}")
    print(f"Subject: {message.subject}")
    print(message.content)
    print("=====================")

    # 5. Save email log
    email_log = EmailLog(
        lead_id=lead.id,
        subject=message.subject,
        body=message.content,
        sent_at=datetime.utcnow()
    )
    db.add(email_log)

    # 6. Update lead status
    lead.status = LeadStatus.CONTACTED.value

    db.commit()

    return {
        "message": "Email sent successfully",
        "lead_status": lead.status
    }
