# 🔐 OTP Authentication API – Football App

This is a backend service built with **FastAPI** for generating and validating **One-Time Passwords (OTP)** via email. It's designed for secure player onboarding in a football training app.

---

## ✅ Features

- 🔹 Generate OTP and send it to player's email
- 🔹 Store OTP in SQLite database with 5-minute expiry
- 🔹 Validate OTP submitted by the user
- 🔹 Optional: View OTP details for testing
- 🔹 Email is sent securely using Gmail's App Password system

---

## 🚀 Technologies Used

| Component        | Tech           |
|------------------|----------------|
| Framework        | FastAPI        |
| Database         | SQLite + SQLAlchemy |
| Email Service    | Gmail (SMTP)   |
| Language         | Python 3.10+   |
| API Docs         | Swagger UI     |

---

## 📂 Project Structure

otp_generation/
├── otp_api.py # Main FastAPI app
├── otp.db # SQLite database storing OTPs
├── requirements.txt # Project dependencies
└── README.md # Project info

yaml
Copy
Edit

---

## ⚙️ Setup & Run

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/your-username/otp-auth-api.git
cd otp-auth-api
2️⃣ Create a Virtual Environment
bash
Copy
Edit
conda create -n football python=3.10 -y
conda activate football
3️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Configure Gmail App Password
You need to set your own Gmail and App Password:

python
Copy
Edit
# In otp_api.py
EMAIL_FROM = "your_email@gmail.com"
EMAIL_PASSWORD = "your_16_char_app_password"
5️⃣ Run the FastAPI Server
bash
Copy
Edit
uvicorn otp_api:app --reload
Swagger UI: http://127.0.0.1:8000/docs

📬 API Endpoints
Method	Endpoint	Description
POST	/v1/player/{player_id}/otp	Generate & email OTP
POST	/v1/player/{player_id}/otp/validate	Validate submitted OTP
GET	/v1/player/{player_id}/otp	View OTP (for testing)

🧪 Sample JSON
📤 Generate OTP
json
Copy
Edit
POST /v1/player/123/otp
{
  "email": "player@example.com"
}
✅ Validate OTP
json
Copy
Edit
POST /v1/player/123/otp/validate
{
  "email": "player@example.com",
  "otp": "123456"
}
📌 Notes
OTPs expire in 5 minutes.

OTPs are sent using SMTP Gmail.

Emails must be valid to receive OTP.

📃 License
MIT License © 2025

