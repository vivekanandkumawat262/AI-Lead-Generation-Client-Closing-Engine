from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import EmailLog

router = APIRouter(prefix="/email-logs", tags=["Email Logs"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{lead_id}")
def get_email_logs(lead_id: int, db: Session = Depends(get_db)):
    return db.query(EmailLog).filter(EmailLog.lead_id == lead_id).all()
