from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import SecurityHeadersMiddleware, RateLimitMiddleware, RequestIDMiddleware
from app.api.v1.endpoints import auth, oauth2, registration, otp, user

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Custom Middleware
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestIDMiddleware)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(oauth2.router, prefix=f"{settings.API_V1_STR}/auth", tags=["oauth2"])
app.include_router(registration.router, prefix=f"{settings.API_V1_STR}/registration", tags=["registration"])
app.include_router(otp.router, prefix=f"{settings.API_V1_STR}/otp", tags=["otp"])
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/user", tags=["user"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
