import hmac
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine, Base
from app.core.rate_limit import rate_limiter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AIIA CTMS API...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified.")
    yield
    logger.info("Shutting down AIIA CTMS API...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AIIA Clinical Trials Dashboard - A comprehensive CTMS for Ayurveda research with CDISC/FHIR interoperability, role-based KPIs, ethics and regulatory tracking, and integrated pharmacovigilance.",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT.lower() != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT.lower() != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
if settings.HTTPS_ONLY:
    app.add_middleware(HTTPSRedirectMiddleware)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    is_auth_route = request.url.path.startswith(f"{settings.API_V1_STR}/auth/")
    limit = settings.AUTH_RATE_LIMIT_REQUESTS if is_auth_route else settings.RATE_LIMIT_REQUESTS
    if not rate_limiter.allow(f"{client_ip}:{'auth' if is_auth_route else 'api'}", limit, settings.RATE_LIMIT_WINDOW_SECONDS):
        return JSONResponse(status_code=429, content={"detail": "Too many requests. Please try again later."})

    unsafe_method = request.method in {"POST", "PUT", "PATCH", "DELETE"}
    csrf_exempt = {f"{settings.API_V1_STR}/auth/login", f"{settings.API_V1_STR}/auth/refresh"}
    if unsafe_method and request.url.path.startswith(settings.API_V1_STR) and request.url.path not in csrf_exempt and request.cookies.get("access_token"):
        cookie_token = request.cookies.get("csrf_token", "")
        header_token = request.headers.get("X-CSRF-Token", "")
        if not cookie_token or not hmac.compare_digest(cookie_token, header_token):
            return JSONResponse(status_code=403, content={"detail": "CSRF validation failed"})

    start = time.time()
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    if settings.HTTPS_ONLY:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")
    return response

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AIIA CTMS API", "version": settings.VERSION}

@app.get("/ready")
async def readiness_check():
    return {"status": "ready"}
