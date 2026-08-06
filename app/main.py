from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from pathlib import Path

from app.api.stl import router as stl_router
from app.api.upload import router as upload_router
from app.api.analysis import router as analysis_router
from app.api.volume import router as volume_router
from app.api.auth import router as auth_router
from app.api.export import router as export_router
from app.database.connection import get_connection

app = FastAPI(title="Dental AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static folder
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Register API routers
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(volume_router)
app.include_router(stl_router)
app.include_router(export_router)


# ── Page routes ──────────────────────────────────────────────

def html(name: str):
    path = Path("app/static") / f"{name}.html"
    return HTMLResponse(path.read_text(encoding="utf-8"))

@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
def page_login():
    return html("login")

@app.get("/signup", response_class=HTMLResponse)
def page_signup():
    return html("signup")

@app.get("/dashboard", response_class=HTMLResponse)
def page_dashboard():
    return html("dashboard")

@app.get("/upload", response_class=HTMLResponse)
def page_upload():
    return html("upload")

@app.get("/results", response_class=HTMLResponse)
def page_results():
    return html("results")

@app.get("/history", response_class=HTMLResponse)
def page_history():
    return html("history")

@app.get("/workflow", response_class=HTMLResponse)
def page_workflow():
    return html("workflow")

@app.get("/viewer", response_class=HTMLResponse)
def page_viewer():
    return html("viewer")

@app.get("/refine", response_class=HTMLResponse)
def page_refine():
    return html("refine")

@app.get("/forgot-password", response_class=HTMLResponse)
def page_forgot_password():
    return html("forgot-password")

@app.get("/reset-password", response_class=HTMLResponse)
def page_reset_password():
    return html("reset-password")


# ── Extra API endpoints ───────────────────────────────────────

@app.get("/scans")
def get_all_scans():
    """Return all scans for the history page."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM scans ORDER BY created_at DESC LIMIT 50")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        # Convert datetime to string for JSON serialisation
        for r in rows:
            if r.get("created_at"):
                r["created_at"] = str(r["created_at"])
        return {"scans": rows}
    except Exception as e:
        return {"scans": [], "error": str(e)}


@app.get("/results-img")
def serve_result_image(path: str):
    """Serve a segmentation image from the results folder."""
    p = Path(path)
    if p.exists():
        return FileResponse(str(p), media_type="image/png")
    return {"error": "Image not found"}


@app.get("/health")
def health():
    return {"message": "Dental AI Backend Running", "version": "1.0.0"}
