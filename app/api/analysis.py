from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pathlib import Path

from app.services.analysis_service import analyze_scan
from app.database.connection import get_connection

router = APIRouter()


def _get_filepath(scan_id: int) -> str:
    """Fetch the uploaded file path for a given scan ID from DB."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT filepath FROM scans WHERE id = %s", (scan_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise ValueError(f"Scan #{scan_id} not found in database")
    return row["filepath"]


@router.post("/analyze/{scan_id}")
def analyze(scan_id: int):
    try:
        filepath = _get_filepath(scan_id)
        result = analyze_scan(filepath, scan_id)
        return {
            "scan_id": scan_id,
            "status":  "analysis_completed",
            "analysis": result
        }
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
