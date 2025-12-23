from app.database import SessionLocal
from app.models import User
from app.core.security import hash_password

db = SessionLocal()

admin = User(
    email="admin@crm.com",
    password_hash=hash_password("admin123"),
    role="ADMIN"
)

db.add(admin)
db.commit()
db.close()

print("Admin user created")
