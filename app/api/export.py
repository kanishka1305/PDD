import numpy as np
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

from app.services.dicom_exporter import export_mask_to_dicom
from app.services.stl_exporter import export_stl
from app.services.preprocess_volume import normalize_volume
from app.services.segmentation import run_full_segmentation, partition_mandible_7_regions
from app.services.metrics import calculate_volume
from app.database.connection import get_connection

router = APIRouter()

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

VALID_REGIONS = {
    "full",
    "condylar_head_L", "condylar_head_R",
    "coronoid_L",      "coronoid_R",
    "angle_ramus_L",   "angle_ramus_R",
    "body_L",          "body_R",
    "symphyseal_parasymphyseal",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_scan_filepath(scan_id: int) -> str:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT filepath FROM scans WHERE id = %s", (scan_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if not row:
        raise ValueError(f"Scan #{scan_id} not found in database")
    return row["filepath"]


def _load_volume(scan_id: int) -> np.ndarray:
    import pydicom
    filepath = Path(_get_scan_filepath(scan_id))

    if filepath.suffix.lower() == ".dcm":
        ds = pydicom.dcmread(str(filepath))
        arr = ds.pixel_array.astype(np.float32)
        if arr.ndim == 2:
            arr = arr[np.newaxis, ...]
        return normalize_volume(arr)

    elif filepath.suffix.lower() in (".nii", ".gz"):
        import nibabel as nib
        img = nib.load(str(filepath))
        data = np.array(img.dataobj).astype(np.float32)
        if data.ndim == 3:
            data = np.moveaxis(data, -1, 0)
        return normalize_volume(data)

    elif filepath.is_dir():
        from app.services.volume_loader import load_dicom_series
        return normalize_volume(load_dicom_series(str(filepath)))

    else:
        import pydicom
        ds = pydicom.dcmread(str(filepath))
        arr = ds.pixel_array.astype(np.float32)
        if arr.ndim == 2:
            arr = arr[np.newaxis, ...]
        return normalize_volume(arr)


def _get_all_masks(scan_id: int) -> dict:
    volume = _load_volume(scan_id)
    full_mask, regions = run_full_segmentation(volume)
    return {"full": full_mask, **regions}


def _stl_path(scan_id: int, region: str) -> Path:
    if region == "full":
        return RESULTS_DIR / f"scan_{scan_id}.stl"
    return RESULTS_DIR / f"scan_{scan_id}_{region}.stl"


def _dcm_path(scan_id: int, region: str) -> Path:
    return RESULTS_DIR / f"scan_{scan_id}_{region}.dcm"


# ── Per-region STL ────────────────────────────────────────────────────────────

@router.get("/stl-region/{scan_id}/{region}")
def download_region_stl(scan_id: int, region: str):
    if region not in VALID_REGIONS:
        return JSONResponse({"error": f"Invalid region. Valid: {sorted(VALID_REGIONS)}"}, status_code=400)

    cached = _stl_path(scan_id, region)
    if cached.exists():
        return FileResponse(str(cached), media_type="application/octet-stream", filename=cached.name)

    try:
        masks = _get_all_masks(scan_id)
        label = str(scan_id) if region == "full" else f"{scan_id}_{region}"
        out = export_stl(masks[region], label)
        if not out:
            return JSONResponse({"error": f"Region '{region}' has no bone voxels"}, status_code=404)
        return FileResponse(out, media_type="application/octet-stream", filename=Path(out).name)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# ── Per-region DICOM ──────────────────────────────────────────────────────────

@router.get("/export-dicom/{scan_id}/{region}")
def export_region_dicom(scan_id: int, region: str):
    if region not in VALID_REGIONS:
        return JSONResponse({"error": f"Invalid region."}, status_code=400)

    cached = _dcm_path(scan_id, region)
    if cached.exists():
        return FileResponse(str(cached), media_type="application/dicom", filename=cached.name)

    try:
        masks = _get_all_masks(scan_id)
        out = export_mask_to_dicom(masks[region], scan_id, region)
        if not out:
            return JSONResponse({"error": f"Region '{region}' has no voxels"}, status_code=404)
        return FileResponse(out, media_type="application/dicom", filename=Path(out).name)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
