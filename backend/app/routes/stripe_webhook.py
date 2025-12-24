import stripe
import os
from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Lead, Payment, LeadStatus

router = APIRouter(prefix="/stripe", tags=["Stripe Webhook"])

endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        lead_id = session["metadata"]["lead_id"]

        db = SessionLocal()
        lead = db.query(Lead).filter(Lead.id == lead_id).first()

        if lead:
            lead.status = LeadStatus.PAID.value
            db.commit()

        db.close()

    return {"status": "success"}
