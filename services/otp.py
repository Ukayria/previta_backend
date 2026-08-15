import random
import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# In-memory OTP store
otp_store = {}
OTP_EXPIRY_SECONDS = 300  # 5 minutes


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def store_otp(identifier: str, otp: str):
    otp_store[identifier] = {
        "otp": otp,
        "expires_at": time.time() + OTP_EXPIRY_SECONDS,
    }


def verify_otp_code(identifier: str, otp: str) -> bool:
    record = otp_store.get(identifier)
    if not record:
        return False
    if time.time() > record["expires_at"]:
        del otp_store[identifier]
        return False
    if record["otp"] != otp:
        return False
    del otp_store[identifier]
    return True


def send_otp_email(email: str, otp: str) -> bool:
    """Send OTP via Gmail SMTP — primary channel"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Your PreVita Verification Code"
        msg["From"] = os.getenv("SMTP_EMAIL")
        msg["To"] = email

        html = f"""
        <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 32px;">
            <div style="background: #1B5E3B; padding: 24px; border-radius: 12px; text-align: center; margin-bottom: 24px;">
                <h1 style="color: white; margin: 0; font-size: 24px;">PreVita</h1>
                <p style="color: rgba(255,255,255,0.8); margin: 8px 0 0;">Health. Prevention. Care.</p>
            </div>
            <h2 style="color: #1A1A1A;">Your verification code</h2>
            <p style="color: #555;">Enter this 6-digit code to verify your identity:</p>
            <div style="background: #F5F5F5; border-radius: 12px; padding: 24px; text-align: center; margin: 24px 0;">
                <span style="font-size: 40px; font-weight: 700; letter-spacing: 12px; color: #1B5E3B;">{otp}</span>
            </div>
            <p style="color: #555;">This code expires in <strong>5 minutes</strong>.</p>
            <p style="color: #999; font-size: 13px;">If you did not request this, please ignore this email.</p>
            <div style="border-top: 1px solid #eee; margin-top: 32px; padding-top: 16px;">
                <p style="color: #999; font-size: 12px; text-align: center;">PreVita — Prevention Before Cure</p>
            </div>
        </div>
        """

        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASSWORD"))
            server.sendmail(os.getenv("SMTP_EMAIL"), email, msg.as_string())

        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False