"""
Generate a synthetic DICOM file for Load Testing.
This guarantees that tests have valid .dcm data in CI/CD environments 
without committing large files or real Patient Health Information (PHI).
"""

import os
from pathlib import Path

try:
    import pydicom
    from pydicom.dataset import FileDataset, FileMetaDataset
    from pydicom.uid import UID
    import numpy as np
except ImportError:
    pass

def create_synthetic_dicom(output_path: Path):
    """Generates a small 10x10x10 synthetic CBCT/DICOM file."""
    
    # Check if pydicom is available, otherwise skip 
    # (used during github actions setup)
    try:
        import pydicom
    except ImportError:
        print("pydicom not installed. Skipping synthetic DICOM generation.")
        return

    print(f"Generating synthetic DICOM at {output_path}...")
    
    # 1. Create Meta info
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = UID('1.2.840.10008.5.1.4.1.1.2') # CT Image Storage
    file_meta.MediaStorageSOPInstanceUID = UID("1.2.3")
    file_meta.ImplementationClassUID = UID("1.2.3.4")

    # 2. Create the Dataset instance
    ds = FileDataset(str(output_path), {}, file_meta=file_meta, preamble=b"\0" * 128)

    # 3. Add necessary elements
    ds.PatientName = "Synthetic^LoadTest"
    ds.PatientID = "LT-001"
    ds.Modality = "CT"
    ds.StudyInstanceUID = "1.2.3.4.5"
    ds.SeriesInstanceUID = "1.2.3.4.5.6"
    ds.SOPInstanceUID = "1.2.3"
    ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.2"
    
    # Image formatting
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 1  # Signed
    ds.HighBit = 15
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.Columns = 10
    ds.Rows = 10
    # Simulate a small 3D volume by making a 2D image but representing one slice 
    # (or 3D array if the backend supports multi-frame, but standard CT is 2D per slice).
    # We will just write a 2D 10x10 image.
    
    # Create random noise to simulate tissue
    pixel_array = np.random.randint(-1000, 1000, size=(10, 10), dtype=np.int16)
    
    ds.PixelData = pixel_array.tobytes()
    ds.is_little_endian = True
    ds.is_implicit_VR = True

    # 4. Save
    ds.save_as(str(output_path))
    print(f"Successfully generated {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    out_dir = Path(__file__).parent
    create_synthetic_dicom(out_dir / "synthetic_jaw.dcm")
