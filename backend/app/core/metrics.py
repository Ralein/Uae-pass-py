from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response

# Defines
AUTH_SUCCESS = Counter("auth_success_total", "Total successful logins", ["method"])
AUTH_FAILURE = Counter("auth_failure_total", "Total failed logins", ["method", "reason"])
OTP_GENERATED = Counter("otp_generated_total", "Total OTPs generated")
OTP_VERIFIED = Counter("otp_verified_total", "Total OTPs verified")
OTP_FAILED = Counter("otp_failed_total", "Total OTPs failed")
RISK_BLOCK = Counter("risk_block_total", "Total requests blocked by risk engine", ["reason"])

REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"])

# Endpoint
router = APIRouter()

@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
