from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Lead, LeadStatus, EmailLog
from ..services.email_service import send_email

router = APIRouter(prefix="/outreach", tags=["Outreach"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/send")
def send_outreach(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    email = (
        db.query(EmailLog)
        .filter(EmailLog.lead_id == lead_id)
        .order_by(EmailLog.sent_at.desc())
        .first()
    )

    if not email:
        raise HTTPException(status_code=400, detail="No email generated for this lead")

    try:
        send_email(
            to_email=lead.email,
            subject=email.subject,
            body=email.body,
        )

        # Update lead status AFTER successful send
        lead.status = LeadStatus.CONTACTED.value

        db.commit()

        return {
            "message": "Email sent successfully",
            "lead_id": lead.id,
            "status": lead.status
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))





# from ..dependencies.auth import get_current_user
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime

# from ..database import SessionLocal
# from ..models import Lead, LeadStatus, Message, EmailLog
# from ..schemas import OutreachResponse
# from app.dependencies.roles import require_role
# from app.core.roles import Role
# from ..services.email_service import send_email


# router = APIRouter(prefix="/outreach", tags=["Outreach"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/send", response_model=OutreachResponse)
# def send_email(lead_id: int, db: Session = Depends(get_db),
#     user=Depends(require_role([Role.ADMIN, Role.AGENT]))):
#     # 1. Fetch lead
#     lead = db.query(Lead).filter(Lead.id == lead_id).first()
#     if not lead:
#         raise HTTPException(status_code=404, detail="Lead not found")

#     # 2. Enforce status rule
#     if lead.status != LeadStatus.NEW.value:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Cannot send email when lead status is {lead.status}"
#         )

#     # 3. Get latest AI-generated message
#     message = (
#         db.query(Message)
#         .filter(Message.lead_id == lead.id)
#         .order_by(Message.created_at.desc())
#         .first()
#     )

#     if not message:
#         raise HTTPException(
#             status_code=400,
#             detail="No AI-generated email found for this lead"
#         )

#     # 4. MOCK EMAIL SEND (replace with SMTP later)
#     print("=== SENDING EMAIL ===")
#     print(f"To: {lead.email}")
#     print(f"Subject: {message.subject}")
#     print(message.content)
#     print("=====================")

#     # 5. Save email log
#     email_log = EmailLog(
#         lead_id=lead.id,
#         subject=message.subject,
#         body=message.content,
#         sent_at=datetime.utcnow()
#     )
#     message_log = Message(
#         lead_id=lead.id,
#         subject=message.subject,
#         content=message.content 
#     )
#     db.add(message_log)
#     db.add(email_log)

#     # 6. Update lead status
#     lead.status = LeadStatus.CONTACTED.value

#     try:
#         send_email(
#             to_email=lead.email,
#             subject=email_log.subject,
#             body=email_log.body,
#         )

#         email_log.status = "SENT"
#         lead.status = LeadStatus.CONTACTED.value

#     except Exception as e:
#         email_log.status = "FAILED"
#         email_log.error = str(e)
#         db.commit()
#         raise HTTPException(status_code=500, detail=str(e))

#     db.commit()
#     return {
#         "message": "Email sent successfully",
#         "lead_id": lead.id,
#         "status": email_log.status,
#     }
