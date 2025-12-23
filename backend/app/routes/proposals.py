from ..dependencies.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Lead, LeadStatus, Proposal
from ..schemas import ProposalResponse
from app.dependencies.roles import require_role
from app.core.roles import Role



router = APIRouter(prefix="/proposals", tags=["Proposals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{lead_id}", response_model=ProposalResponse)
def generate_proposal(lead_id: int, db: Session = Depends(get_db),
    user=Depends(require_role([Role.ADMIN, Role.AGENT]))):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if lead.status != LeadStatus.INTERESTED.value:
        raise HTTPException(
            status_code=400,
            detail="Proposal can be generated only for INTERESTED leads"
        )

    # MOCK AI PROPOSAL
    proposal_text = f"""
Digital Marketing Proposal for {lead.business_name}

Services:
- SEO Optimization
- Google Ads
- Social Media Marketing

Expected Results:
- 30–50 new leads per month

Monthly Price:
₹30,000 / month

Regards,
Cyberweb Agency
"""

    proposal = Proposal(
        lead_id=lead.id,
        content=proposal_text
    )

    lead.status = LeadStatus.PROPOSAL_SENT.value

    db.add(proposal)
    db.commit()

    return {
        "proposal": proposal_text,
        "lead_status": lead.status
    }
