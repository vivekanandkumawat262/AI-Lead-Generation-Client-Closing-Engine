# app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from enum import Enum
from .database import Base
from sqlalchemy import ForeignKey


class LeadStatus(str, Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    INTERESTED = "INTERESTED"
    PROPOSAL_SENT = "PROPOSAL_SENT"
    PAID = "PAID"


# app/models.py (continue)
class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    industry = Column(String, nullable=False)
    city = Column(String, nullable=False)
    status = Column(String, default=LeadStatus.NEW.value)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# app/models.py (add below Lead model)
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer)
    subject = Column(String)
    content = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer)
    content = Column(String, nullable=False)
    intent = Column(String, nullable=False)  # INTERESTED / NOT_INTERESTED
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer)
    stripe_payment_intent = Column(String)
    amount = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
