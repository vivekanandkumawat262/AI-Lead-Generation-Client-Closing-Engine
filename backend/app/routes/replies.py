from ..dependencies.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Lead, LeadStatus, Reply
from ..schemas import ReplyRequest, ReplyResponse
from app.dependencies.roles import require_role
from app.core.roles import Role


router = APIRouter(prefix="/replies", tags=["Replies"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{lead_id}", response_model=ReplyResponse)
def classify_reply(lead_id: int, reply: ReplyRequest, db: Session = Depends(get_db),
    user=Depends(require_role([Role.ADMIN, Role.AGENT]))):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if lead.status != LeadStatus.CONTACTED.value:
        raise HTTPException(
            status_code=400,
            detail="Replies allowed only when lead is CONTACTED"
        )

    text = reply.content.lower()

    # SIMPLE AI LOGIC (mock – replace later with GPT)
    if any(word in text for word in ["price", "cost", "interested", "details", "yes"]):
        intent = "INTERESTED"
        lead.status = LeadStatus.INTERESTED.value
    else:
        intent = "NOT_INTERESTED"

    reply_entry = Reply(
        lead_id=lead.id,
        content=reply.content,
        intent=intent
    )

    db.add(reply_entry)
    db.commit()

    return {
        "intent": intent,
        "lead_status": lead.status
    }
