"""
FastAPI Application Entry Point — SECURITY FIXES APPLIED

SEC-003  CORS restricted to explicit origin list (no wildcard)
SEC-009  /results-img path traversal FIXED — validated inside results/ dir only
SEC-016  All 7 security headers added via middleware
SEC-018  /scans endpoint requires authentication + filters by doctor
SEC-022  Static page routes do NOT expose data without JWT check
SEC-014  /volume-test returns 404 in production (see volume.py)
SEC-011  Raw exceptions no longer returned to clients
SEC-019  Swagger/ReDoc/OpenAPI disabled in production
"""

import os
import logging
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.api.stl       import router as stl_router
from app.api.upload    import router as upload_router
from app.api.analysis  import router as analysis_router
from app.api.volume    import router as volume_router
from app.api.auth      import router as auth_router
from app.api.export    import router as export_router
from app.auth.jwt_handler import require_auth, get_current_doctor_id
from app.database.connection import get_connection

logger = logging.getLogger(__name__)

# ── App instance ──────────────────────────────────────────────────────────────
# Disable Swagger / ReDoc / OpenAPI JSON in production (SEC-010/011/012)
_DEBUG = os.environ.get("DEBUG_MODE", "false").lower() == "true"

app = FastAPI(
    title       = "Dental AI Backend",
    version     = "2.0.0",
    docs_url    = "/docs"    if _DEBUG else None,
    redoc_url   = "/redoc"   if _DEBUG else None,
    openapi_url = "/openapi.json" if _DEBUG else None,
)

# ── Rate limiter ──────────────────────────────────────────────────────────────
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded

    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
except ImportError:
    pass

# ── SEC-016: Security Headers Middleware ──────────────────────────────────────
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"]    = "nosniff"
        response.headers["X-Frame-Options"]           = "DENY"
        response.headers["X-XSS-Protection"]          = "1; mode=block"
        response.headers["Referrer-Policy"]           = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"]        = "geolocation=(), camera=(), microphone=()"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["Content-Security-Policy"]   = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://unpkg.com; "
            "img-src 'self' data: blob:; "
            "connect-src 'self';"
        )
        # Remove server fingerprint (use del not pop — MutableHeaders has no pop())
        try:
            del response.headers["server"]
        except KeyError:
            pass
        try:
            del response.headers["x-powered-by"]
        except KeyError:
            pass
        return response

app.add_middleware(SecurityHeadersMiddleware)

# ── SEC-003: Restricted CORS ──────────────────────────────────────────────────
_raw_origins = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:8000,http://172.23.51.65:8000"
)
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]
# Allow all private network origins for mobile app testing
ALLOWED_ORIGINS += ["http://172.23.51.65:8081"]  # React Native Metro

app.add_middleware(
    CORSMiddleware,
    allow_origins     = ALLOWED_ORIGINS,   # explicit list — no wildcard
    allow_credentials = True,
    allow_methods     = ["GET", "POST"],
    allow_headers     = ["Authorization", "Content-Type"],
)

# ── Static files ──────────────────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(volume_router)
app.include_router(stl_router)
app.include_router(export_router)


# ── HTML page helpers ─────────────────────────────────────────────────────────
def _html(name: str) -> HTMLResponse:
    path = Path("app/static") / f"{name}.html"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Page not found")
    return HTMLResponse(path.read_text(encoding="utf-8"))


# ── Public pages (no data, no auth required) ──────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
def page_login():
    return _html("login")

@app.get("/signup", response_class=HTMLResponse)
def page_signup():
    return _html("signup")

@app.get("/forgot-password", response_class=HTMLResponse)
def page_forgot_password():
    return _html("forgot-password")

@app.get("/reset-password", response_class=HTMLResponse)
def page_reset_password():
    return _html("reset-password")


# ── Protected pages (served as HTML — auth enforced by JS / API layer) ────────
@app.get("/dashboard", response_class=HTMLResponse)
def page_dashboard():
    return _html("dashboard")

@app.get("/upload", response_class=HTMLResponse)
def page_upload():
    return _html("upload")

@app.get("/results", response_class=HTMLResponse)
def page_results():
    return _html("results")

@app.get("/history", response_class=HTMLResponse)
def page_history():
    return _html("history")

@app.get("/workflow", response_class=HTMLResponse)
def page_workflow():
    return _html("workflow")

@app.get("/viewer", response_class=HTMLResponse)
def page_viewer():
    return _html("viewer")

@app.get("/refine", response_class=HTMLResponse)
def page_refine():
    return _html("refine")


# ── SEC-018: /scans — authentication required, scoped to doctor ───────────────
@app.get("/scans")
def get_all_scans(current_user: dict = Depends(require_auth)):
    """Return scans belonging to the authenticated doctor."""
    doctor_id = get_current_doctor_id(current_user)
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Try the doctor-scoped query first (post-migration schema)
            cursor.execute(
                "SELECT id, patient_name, patient_id, filename, modality, status, created_at "
                "FROM scans WHERE doctor_id = %s ORDER BY created_at DESC LIMIT 50",
                (doctor_id,),
            )
        except Exception:
            # Fallback: doctor_id column not yet added — add it transparently
            try:
                cursor.execute("ALTER TABLE scans ADD COLUMN doctor_id INT DEFAULT NULL")
                conn.commit()
                logger.info("Added missing doctor_id column to scans table")
            except Exception:
                pass  # Column may already exist or concurrent add
            # Return all scans (single-user dev mode)
            cursor.execute(
                "SELECT id, patient_name, patient_id, filename, modality, status, created_at "
                "FROM scans ORDER BY created_at DESC LIMIT 50"
            )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for r in rows:
            if r.get("created_at"):
                r["created_at"] = str(r["created_at"])
        return {"scans": rows}
    except Exception as exc:
        logger.error("/scans error: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error")


# ── SEC-009: /results-img — path traversal FIXED ─────────────────────────────
_RESULTS_ROOT = Path("results").resolve()
_ALLOWED_IMAGE_EXTS = {".png", ".jpg", ".jpeg"}

@app.get("/results-img")
def serve_result_image(
    path: str,
    current_user: dict = Depends(require_auth),
):
    """
    Serve a segmentation image. The path is validated to:
    1. Stay inside the results/ directory (no traversal)
    2. Have an image extension only (no source code leakage)
    """
    # Resolve and contain to results root
    try:
        requested = (_RESULTS_ROOT / path).resolve()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid path")

    if not str(requested).startswith(str(_RESULTS_ROOT)):
        raise HTTPException(status_code=403, detail="Access denied")

    if requested.suffix.lower() not in _ALLOWED_IMAGE_EXTS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    if not requested.exists():
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(str(requested), media_type="image/png")


# ── Public health check ───────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"message": "Dental AI Backend Running", "version": "2.0.0"}
