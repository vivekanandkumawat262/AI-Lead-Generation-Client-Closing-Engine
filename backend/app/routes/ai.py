from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Lead, Message
from ..schemas import AIEmailResponse

router = APIRouter(prefix="/ai", tags=["AI"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/email", response_model=AIEmailResponse)
def generate_email(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # MOCK AI RESPONSE (we replace later with OpenAI)
    subject = f"Helping {lead.business_name} get more customers"
    body = f"""
Hi,

I came across {lead.business_name} in {lead.city}.
We help {lead.industry} businesses get more customers using digital marketing.

Would you like to know more?

Regards,
Cyberweb
"""

    message = Message(
        lead_id=lead.id,
        subject=subject,
        content=body
    )
    db.add(message)
    db.commit()

    return {"subject": subject, "body": body}
