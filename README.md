# ⚽ Football App - OTP Backend API (FastAPI + PostgreSQL + SendGrid)

This backend service handles OTP (One-Time Password) generation, email delivery, and validation for player registration and login within a football training app.

---

## 🚀 Features

- Player registration with email
- OTP generation with 5-minute expiry
- Email delivery via SendGrid API
- OTP validation flow
- PostgreSQL database integration
- REST API built with FastAPI

---

## 🛠 Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- SendGrid (email service)
- Python 3.10+

---

## 📁 Project Structure

otp_generation/
│
├── otp_api.py # Main FastAPI app
├── .env # Environment variables
├── requirements.txt # Python dependencies
├── README.md # Project documentation



---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Likitha0424/football-otp-backend.git
cd football-otp-backend
2. Create & Activate Virtual Environment
bash

conda create -n football python=3.10 -y
conda activate football
3. Create .env File
Create a .env file in the root folder and add:

ini


4. Install Dependencies
bash

pip install -r requirements.txt
5. Run the FastAPI App
bash

uvicorn otp_api:app --reload
📡 API Endpoints
Method	Endpoint	Description
POST	/v1/player/register	Register a new player
POST	/v1/player/{playerId}/otp	Generate and send OTP to email
GET	/v1/player/{playerId}/otp	Retrieve OTP info
POST	/v1/player/{playerId}/otp/validate	Validate player OTP

✅ Flow Summary
Player registers using email

OTP is generated and emailed

Player enters OTP on frontend

OTP is validated via /validate

On success, player is marked active

👩‍💻 Author
Likitha0424 – GitHub Profile