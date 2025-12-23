from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.dependencies.roles import require_role
from app.core.roles import Role

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_users(
    db: Session = Depends(get_db),
    user=Depends(require_role([Role.ADMIN]))
):
    return db.query(User).all()
