import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian
from pydicom.sequence import Sequence
from pathlib import Path
import datetime

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


def export_mask_to_dicom(mask: np.ndarray, scan_id, region_name: str = "full") -> str:
    """
    Convert a 3-D binary mask (slices × rows × cols) into a multi-frame
    DICOM file and save it to results/.
    Returns the file path string.
    """
    if mask.ndim != 3 or np.sum(mask) == 0:
        return ""

    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S.%f")

    out_path = RESULTS_DIR / f"scan_{scan_id}_{region_name}.dcm"

    # Build one DICOM file per slice, package as enhanced multi-frame
    slices = []
    for i in range(mask.shape[0]):
        slice_data = (mask[i] * 255).astype(np.uint8)
        slices.append(slice_data)

    # Use the first slice as the template
    ds = FileDataset(str(out_path), {}, is_implicit_VR=False, is_little_endian=True)

    # ── Required DICOM metadata ──────────────────────────────────
    ds.file_meta = Dataset()
    ds.file_meta.MediaStorageSOPClassUID    = "1.2.840.10008.5.1.4.1.1.2"   # CT Image Storage
    ds.file_meta.MediaStorageSOPInstanceUID = generate_uid()
    ds.file_meta.TransferSyntaxUID          = ExplicitVRLittleEndian

    ds.is_implicit_VR  = False
    ds.is_little_endian = True

    ds.SOPClassUID       = "1.2.840.10008.5.1.4.1.1.2"
    ds.SOPInstanceUID    = ds.file_meta.MediaStorageSOPInstanceUID
    ds.StudyInstanceUID  = generate_uid()
    ds.SeriesInstanceUID = generate_uid()

    ds.PatientName  = "DentAI Patient"
    ds.PatientID    = f"SCAN_{scan_id}"
    ds.StudyDate    = date_str
    ds.StudyTime    = time_str
    ds.ContentDate  = date_str
    ds.ContentTime  = time_str
    ds.Modality     = "CT"
    ds.Manufacturer = "DentAI Platform"

    ds.SeriesDescription = f"Mandible Segmentation — {region_name.title()}"
    ds.StudyDescription  = "Dental AI Segmentation Export"

    ds.Rows    = mask.shape[2]
    ds.Columns = mask.shape[1]

    ds.PixelSpacing          = [1.0, 1.0]
    ds.SliceThickness        = 1.0
    ds.BitsAllocated         = 8
    ds.BitsStored            = 8
    ds.HighBit               = 7
    ds.PixelRepresentation   = 0
    ds.SamplesPerPixel       = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.NumberOfFrames        = mask.shape[0]
    ds.InstanceNumber        = 1

    # Pack all slices into one pixel data blob
    pixel_array = np.stack(slices, axis=0).astype(np.uint8)
    ds.PixelData = pixel_array.tobytes()

    pydicom.dcmwrite(str(out_path), ds)
    return str(out_path)


def export_all_regions_to_dicom(masks: dict, scan_id) -> dict:
    """
    Export every region mask as its own DICOM file.
    masks = { 'full': ndarray, 'condyles': ndarray, ... }
    Returns { region: filepath }
    """
    paths = {}
    for region, mask in masks.items():
        p = export_mask_to_dicom(mask, scan_id, region)
        if p:
            paths[region] = p
    return paths
