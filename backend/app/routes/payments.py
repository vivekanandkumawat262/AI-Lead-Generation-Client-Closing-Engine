import stripe
import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Lead, LeadStatus, Payment
from ..schemas import PaymentLinkResponse

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter(prefix="/payments", tags=["Payments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 Create Payment Link
@router.post("/create/{lead_id}", response_model=PaymentLinkResponse)
def create_payment_link(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if lead.status != LeadStatus.PROPOSAL_SENT.value:
        raise HTTPException(
            status_code=400,
            detail="Payment allowed only after proposal is sent"
        )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "inr",
                    "product_data": {
                        "name": f"Marketing Services for {lead.business_name}",
                    },
                    "unit_amount": 3000000,  # ₹30,000
                },
                "quantity": 1,
            }
        ],
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel",
        metadata={
            "lead_id": str(lead.id)
        }
    )

    return {
        "payment_url": session.url,
        "lead_status": lead.status
    }


# 🔹 Stripe Webhook
@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        lead_id = int(session["metadata"]["lead_id"])

        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if lead:
            lead.status = LeadStatus.PAID.value

            payment = Payment(
                lead_id=lead.id,
                stripe_payment_intent=session["payment_intent"],
                amount=session["amount_total"],
                status="PAID"
            )
            db.add(payment)
            db.commit()

    return {"status": "success"}
