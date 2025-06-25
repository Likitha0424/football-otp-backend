from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from random import randint
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy import create_engine, Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")
DATABASE_URL = os.getenv("DATABASE_URL")

# === Database setup ===
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class OTPRecord(Base):
    __tablename__ = "otp"
    player_id = Column(String, primary_key=True, index=True)
    email = Column(String)
    otp = Column(String)
    expires_at = Column(DateTime)
    retry_count = Column(Integer, default=0)  # NEW

Base.metadata.create_all(bind=engine)

# === FastAPI App ===
app = FastAPI()

# === Pydantic Models ===
class OTPRequest(BaseModel):
    email: EmailStr

class OTPValidate(BaseModel):
    email: EmailStr
    otp: str

# === Email Sender ===
def send_otp_email(email: str, otp: str):
    message = Mail(
        from_email=SENDGRID_FROM_EMAIL,
        to_emails=email,
        subject="Your One-Time Password (OTP)",
        plain_text_content=f"Your OTP is: {otp}\nIt is valid for 5 minutes.\n\n- Football App"
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email send failed: {e}")

# === POST: Generate OTP ===
@app.post("/v1/player/{player_id}/otp")
def generate_otp(player_id: str, req: OTPRequest):
    otp = f"{randint(100000, 999999)}"
    expiry = datetime.utcnow() + timedelta(minutes=5)

    db = SessionLocal()
    # Clear previous OTP (if any)
    db.query(OTPRecord).filter(OTPRecord.player_id == player_id).delete()
    # Create new OTP with retry_count = 0
    db.add(OTPRecord(
        player_id=player_id,
        email=req.email,
        otp=otp,
        expires_at=expiry,
        retry_count=0
    ))
    db.commit()
    db.close()

    send_otp_email(req.email, otp)
    return {"message": "OTP sent to email."}

# === POST: Validate OTP ===
@app.post("/v1/player/{player_id}/otp/validate")
def validate_otp(player_id: str, req: OTPValidate):
    db = SessionLocal()
    record = db.query(OTPRecord).filter(OTPRecord.player_id == player_id).first()

    if not record:
        db.close()
        raise HTTPException(status_code=404, detail="OTP not found.")

    if record.retry_count >= 3:
        db.close()
        raise HTTPException(status_code=403, detail="Maximum OTP attempts exceeded.")

    if record.email != req.email or record.otp != req.otp:
        record.retry_count += 1
        db.commit()
        db.close()
        raise HTTPException(status_code=401, detail="OTP did not match.")

    if datetime.utcnow() > record.expires_at:
        db.close()
        raise HTTPException(status_code=400, detail="OTP expired.")

    # Reset retry count on success
    record.retry_count = 0
    db.commit()
    db.close()

    return {"message": "OTP validated successfully."}

# === GET: View OTP (for testing only) ===
@app.get("/v1/player/{player_id}/otp")
def get_otp(player_id: str):
    db = SessionLocal()
    record = db.query(OTPRecord).filter(OTPRecord.player_id == player_id).first()
    db.close()

    if not record:
        raise HTTPException(status_code=404, detail="OTP not found.")

    return {
        "email": record.email,
        "otp": record.otp,
        "expires_at": record.expires_at.isoformat(),
        "retry_count": record.retry_count
    }
