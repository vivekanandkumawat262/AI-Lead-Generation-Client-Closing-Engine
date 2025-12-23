# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .routes import leads

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM AutoPilot")

app.include_router(leads.router)

@app.get("/")
def root():
    return {"message": "CRM AutoPilot Backend Running"}
