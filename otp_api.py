from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from random import randint
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# === DB Setup ===
DATABASE_URL = "sqlite:///./otp.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class OTPRecord(Base):
    __tablename__ = "otp"

    player_id = Column(String, primary_key=True, index=True)
    email = Column(String)
    otp = Column(String)
    expires_at = Column(DateTime)

Base.metadata.create_all(bind=engine)

# === FastAPI ===
app = FastAPI()

# === Email Setup ===
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "likithap2404@gmail.com"
EMAIL_PASSWORD = "ztvaarqtqpvyqqjf"  # <- your latest 16-char app password (no spaces)

# === Pydantic Schemas ===
class OTPRequest(BaseModel):
    email: EmailStr

class OTPValidate(BaseModel):
    email: EmailStr
    otp: str

# === Helper: Send OTP ===
def send_otp_email(email: str, otp: str):
    subject = "Your One-Time Password (OTP)"
    body = f"Your OTP is: {otp}\nIt is valid for 5 minutes.\n\n- Football App"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, email, msg.as_string())
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

# === POST /otp: Generate and store OTP ===
@app.post("/v1/player/{player_id}/otp")
def generate_otp(player_id: str, req: OTPRequest):
    otp = f"{randint(100000, 999999)}"
    expiry = datetime.utcnow() + timedelta(minutes=5)

    db = SessionLocal()
    db.query(OTPRecord).filter(OTPRecord.player_id == player_id).delete()
    db.add(OTPRecord(player_id=player_id, email=req.email, otp=otp, expires_at=expiry))
    db.commit()
    db.close()

    send_otp_email(req.email, otp)
    return {"message": "OTP sent to email."}

# === POST /validate ===
@app.post("/v1/player/{player_id}/otp/validate")
def validate_otp(player_id: str, req: OTPValidate):
    db = SessionLocal()
    record = db.query(OTPRecord).filter(OTPRecord.player_id == player_id).first()
    db.close()

    if not record:
        raise HTTPException(status_code=404, detail="No OTP found.")

    if record.email != req.email or record.otp != req.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP or email.")

    if datetime.utcnow() > record.expires_at:
        raise HTTPException(status_code=400, detail="OTP expired.")

    return {"message": "OTP validated successfully."}

# === GET /otp: View OTP record (for testing only) ===
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
        "expires_at": record.expires_at.isoformat()
    }
