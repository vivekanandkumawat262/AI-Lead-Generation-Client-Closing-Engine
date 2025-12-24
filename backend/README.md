🚀 AI Lead Generation & Client Closing Engine (Backend)

A production-ready backend for automating lead management, AI email outreach, proposal generation, and payments using FastAPI, Gemini AI, SMTP, and Stripe.

🧠 Features

🔐 JWT Authentication (Admin / Agent roles)

🧾 Lead Management (CRM)

🤖 AI Email Generation (Gemini API)

📧 Send Real Emails (Gmail / Outlook SMTP)

📬 Email Logs

💬 Reply Classification (Interested / Not Interested)

📄 Proposal Generation

💳 Stripe Payment Integration

🗃️ SQLite (easy switch to Postgres)

🧪 Fully testable via Postman

🏗️ Project Structure
backend/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── core/
│   │   ├── security.py
│   │   └── roles.py
│   │
│   ├── dependencies/
│   │   ├── auth.py
│   │   └── roles.py
│   │
│   ├── services/
│   │   ├── ai_email_service.py
│   │   └── email_service.py
│   │
│   └── routes/
│       ├── auth.py
│       ├── leads.py
│       ├── ai.py
│       ├── outreach.py
│       ├── replies.py
│       ├── proposals.py
│       └── payments.py
│
├── create_admin.py
├── list_models.py
├── requirements.txt
├── .env
└── README.md

⚙️ Tech Stack

FastAPI

SQLAlchemy

SQLite (Postgres ready)

JWT Authentication

Google Gemini API

SMTP (Gmail / Outlook)

Stripe

Uvicorn

🧩 STEP 1: Clone & Setup Environment
git clone <your-repo-url>
cd backend
python -m venv venv
venv\Scripts\activate   # Windows

📦 STEP 2: Install Dependencies
pip install -r requirements.txt


If missing:

pip install fastapi uvicorn sqlalchemy python-dotenv passlib[bcrypt] python-jose google-genai stripe email-validator

🔑 STEP 3: Environment Variables

Create .env file:

# JWT
SECRET_KEY=supersecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# SMTP (Gmail example)
SMTP_EMAIL=yourgmail@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# Stripe
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

🗄️ STEP 4: Database Initialization

The database auto-creates tables when server starts.

To create admin user:

python create_admin.py


Default admin:

email: admin@crm.com
password: admin123

▶️ STEP 5: Run Server
uvicorn app.main:app --reload


Open Swagger:

http://127.0.0.1:8000/docs

🔐 AUTH FLOW (IMPORTANT)
Login
POST /auth/login


Body:

{
  "email": "admin@crm.com",
  "password": "admin123"
}


Copy access_token and use in Postman:

Authorization: Bearer <token>

🧾 LEAD FLOW (CORE LOGIC)
Lead Status Lifecycle
NEW → CONTACTED → INTERESTED → PROPOSAL_SENT → PAID

🧪 API TESTING ORDER (POSTMAN)
1️⃣ Create Lead
POST /leads

{
  "business_name": "Royal Spice Restaurant",
  "email": "royalspice@gmail.com",
  "industry": "Restaurant",
  "city": "Sikar"
}

2️⃣ Generate AI Email
POST /ai/email?lead_id=1


✅ Generates subject + body
❌ Does NOT send email

3️⃣ Send Email (SMTP)
POST /outreach/send?lead_id=1


✔️ Sends real email
✔️ Saves email log
✔️ Status → CONTACTED

4️⃣ Classify Reply
POST /replies/1

{
  "content": "Yes, I'm interested"
}


✔️ Status → INTERESTED

5️⃣ Generate Proposal
POST /proposals/1


✔️ Status → PROPOSAL_SENT

6️⃣ Create Stripe Payment
POST /payments/create/1


✔️ Returns Stripe Checkout URL
✔️ Client pays
✔️ Status → PAID (via webhook)

💳 Stripe Setup (Local)

Install Stripe CLI:

stripe login
stripe listen --forward-to localhost:8000/payments/webhook


Copy webhook secret → .env

🧠 AI Email Engine

Uses Gemini models (example):

models/gemini-flash-latest
models/gemini-pro-latest


Model availability checked via:

python list_models.py

🚀 Production Ready Notes

Replace SQLite with Postgres for deployment

Use background tasks for email sending

Add rate limiting

Add retry logic for AI + SMTP

Deploy on Render / Railway / AWS

🏁 Final Status

✅ Authentication
✅ CRM
✅ AI Email
✅ Real Email
✅ Reply Classification
✅ Proposal
✅ Payments
✅ Logs
✅ Production Flow

💼 Project Value

Freelance: ₹50,000 – ₹80,000

SaaS MVP: ₹1,00,000+

Global clients: $1,000 – $2,500

👨‍💻 Author

Vivekanand Kumawat
Backend | AI | SaaS Engineering