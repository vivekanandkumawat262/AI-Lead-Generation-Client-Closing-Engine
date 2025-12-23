from dotenv import load_dotenv
load_dotenv()
# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .routes import leads, ai, outreach, replies, proposals, payments, auth
from .routes import users

 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRM AutoPilot")

app.include_router(leads.router)
app.include_router(ai.router)
app.include_router(outreach.router)
app.include_router(replies.router)
app.include_router(proposals.router)
app.include_router(payments.router)
app.include_router(auth.router)
app.include_router(users.router)



@app.get("/")
def root():
    return {"message": "CRM AutoPilot Backend Running"}



# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "Server OK"}



# from fastapi import FastAPI
# from .database import Base, engine

# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "DB OK"}





# from fastapi import FastAPI
# from .database import Base, engine
# from .routes import leads

# Base.metadata.create_all(bind=engine)

# app = FastAPI()
# app.include_router(leads.router)

# @app.get("/")
# def root():
#     return {"message": "Leads OK"}