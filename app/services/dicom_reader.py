import pydicom


def read_dicom(path: str) -> dict:
    """
    Read DICOM metadata from a file.
    Uses force=True so partially-valid files still open.
    Never raises — returns safe defaults for missing tags.
    """
    try:
        ds = pydicom.dcmread(path, force=True)
    except Exception as e:
        return {
            "patient_name":       "Unknown",
            "patient_id":         "Unknown",
            "study_date":         "Unknown",
            "modality":           "Unknown",
            "rows":               0,
            "columns":            0,
            "slice_thickness":    "Unknown",
            "pixel_spacing":      "Unknown",
            "manufacturer":       "Unknown",
            "study_description":  "Unknown",
            "read_error":         str(e),
        }

    def safe(attr, default="Unknown"):
        val = getattr(ds, attr, default)
        if val is None:
            return default
        return str(val)

    def safe_int(attr, default=0):
        try:
            return int(getattr(ds, attr, default) or default)
        except Exception:
            return default

    return {
        "patient_name":      safe("PatientName"),
        "patient_id":        safe("PatientID"),
        "study_date":        safe("StudyDate"),
        "modality":          safe("Modality"),
        "rows":              safe_int("Rows"),
        "columns":           safe_int("Columns"),
        "slice_thickness":   safe("SliceThickness"),
        "pixel_spacing":     safe("PixelSpacing"),
        "manufacturer":      safe("Manufacturer"),
        "study_description": safe("StudyDescription"),
    }
