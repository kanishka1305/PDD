import os
import numpy as np
import pydicom


def load_dicom_series(folder_path):

    dicom_files = []

    for file in os.listdir(folder_path):

        if file.lower().endswith(".dcm"):

            file_path = os.path.join(folder_path, file)

            ds = pydicom.dcmread(file_path)

            dicom_files.append(ds)

    if len(dicom_files) == 0:
        raise Exception("No DICOM files found")

    dicom_files.sort(
        key=lambda x: int(
            getattr(x, "InstanceNumber", 0)
        )
    )

    volume = np.stack(
        [ds.pixel_array for ds in dicom_files]
    )

    return volume


def get_volume_info(volume):

    return {
        "shape": volume.shape,
        "dtype": str(volume.dtype),
        "min_value": float(volume.min()),
        "max_value": float(volume.max())
    }