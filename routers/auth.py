from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.otp import generate_otp, store_otp, verify_otp_code, send_otp_email

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class SendOTPRequest(BaseModel):
    email: str


class VerifyOTPRequest(BaseModel):
    email: str
    otp: str


class ResendOTPRequest(BaseModel):
    email: str


@router.post("/send-otp")
async def send_otp(request: SendOTPRequest):
    if not request.email:
        raise HTTPException(status_code=400, detail="Email is required.")

    otp = generate_otp()
    store_otp(request.email, otp)
    success = send_otp_email(request.email, otp)

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to send OTP. Please check the email address and try again."
        )

    return {
        "message": f"OTP sent to {request.email}",
        "channel": "email",
        "expires_in": 300,
    }


@router.post("/verify-otp")
async def verify_otp(request: VerifyOTPRequest):
    if not request.email or not request.otp:
        raise HTTPException(status_code=400, detail="Email and OTP are required.")

    is_valid = verify_otp_code(request.email, request.otp)

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP. Please request a new one."
        )

    return {
        "message": "OTP verified successfully.",
        "verified": True,
        "email": request.email,
    }


@router.post("/resend-otp")
async def resend_otp(request: ResendOTPRequest):
    if not request.email:
        raise HTTPException(status_code=400, detail="Email is required.")

    otp = generate_otp()
    store_otp(request.email, otp)
    success = send_otp_email(request.email, otp)

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Failed to resend OTP. Please try again."
        )

    return {
        "message": f"New OTP sent to {request.email}",
        "channel": "email",
        "expires_in": 300,
    }