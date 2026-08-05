from fastapi import APIRouter, UploadFile, File
import shutil
from pathlib import Path

from app.services.preprocess import dicom_to_numpy
from app.services.dicom_reader import read_dicom
from app.services.nifti_reader import read_nifti
from app.database.scan_repository import save_scan

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # ── Save file ────────────────────────────────────────
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        fname_lower = file.filename.lower()

        # ── DICOM ────────────────────────────────────────────
        if fname_lower.endswith(".dcm"):
            metadata = read_dicom(str(file_path))

            # Try to extract pixel array; fall back gracefully
            try:
                image = dicom_to_numpy(str(file_path))
                metadata["image_shape"] = list(image.shape)
                metadata["min_pixel"]   = float(image.min())
                metadata["max_pixel"]   = float(image.max())
            except Exception as px_err:
                # Pixel extraction failed — still allow upload to succeed
                metadata["image_shape"] = [metadata.get("rows", 0),
                                           metadata.get("columns", 0)]
                metadata["min_pixel"]   = 0.0
                metadata["max_pixel"]   = 0.0
                metadata["pixel_warning"] = str(px_err)

            scan_id = save_scan(metadata, file.filename, str(file_path))

        # ── NIfTI ────────────────────────────────────────────
        elif fname_lower.endswith((".nii", ".nii.gz")):
            metadata = read_nifti(str(file_path))
            scan_id  = save_scan(
                {
                    "patient_name": "Unknown",
                    "patient_id":   "Unknown",
                    "modality":     "NIfTI",
                },
                file.filename,
                str(file_path),
            )

        # ── ZIP (DICOM series) ────────────────────────────────
        elif fname_lower.endswith(".zip"):
            import zipfile, tempfile, os
            extract_dir = UPLOAD_DIR / (file.filename + "_extracted")
            extract_dir.mkdir(exist_ok=True)
            with zipfile.ZipFile(str(file_path), "r") as zf:
                zf.extractall(str(extract_dir))
            # Find first DCM inside
            dcm_files = list(extract_dir.rglob("*.dcm"))
            if dcm_files:
                metadata = read_dicom(str(dcm_files[0]))
                metadata["image_shape"] = [0, 0]
                metadata["min_pixel"]   = 0.0
                metadata["max_pixel"]   = 0.0
                metadata["zip_slices"]  = len(dcm_files)
            else:
                metadata = {"patient_name": "Unknown", "patient_id": "Unknown",
                            "modality": "ZIP", "image_shape": [0, 0],
                            "min_pixel": 0.0, "max_pixel": 0.0}
            scan_id = save_scan(metadata, file.filename, str(file_path))

        else:
            return {"error": f"Unsupported file type: {file.filename}"}

        return {
            "scan_id":  scan_id,
            "filename": file.filename,
            "saved_to": str(file_path),
            "metadata": metadata,
        }

    except Exception as e:
        return {"error": str(e)}
