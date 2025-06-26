from otp_api import Base, engine, OTPRecord

# Drop the OTP table if it exists
OTPRecord.__table__.drop(engine)
print("Dropped existing otp table.")

# Recreate it with updated schema
Base.metadata.create_all(bind=engine)
print("Recreated otp table with latest columns.")
