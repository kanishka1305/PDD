import trimesh
import numpy as np
from pathlib import Path
from skimage.measure import marching_cubes

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

_MIN_SLICES = 4   # marching cubes needs depth


def _pad_to_3d(mask: np.ndarray) -> np.ndarray:
    """
    Ensure mask is 3-D with at least _MIN_SLICES in every axis.
    Handles 2-D arrays and single-slice volumes.
    """
    if mask.ndim == 2:
        mask = mask[np.newaxis, ...]

    # Pad each axis that is too thin by repeating the last slice
    for axis in range(3):
        while mask.shape[axis] < _MIN_SLICES:
            pad_slice = np.take(mask, [-1], axis=axis)
            mask = np.concatenate([mask, pad_slice], axis=axis)

    return mask.astype(np.float32)


def export_stl(mask: np.ndarray, scan_id) -> str:
    """
    Export a binary mask as an STL file.
    Returns the file path string, or "" if the mask is empty or export fails.
    """
    if mask is None or np.sum(mask) == 0:
        return ""

    try:
        padded = _pad_to_3d(mask)

        verts, faces, normals, _ = marching_cubes(padded, level=0.5)

        mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=False)

        stl_path = RESULTS_DIR / f"scan_{scan_id}.stl"
        mesh.export(str(stl_path))
        return str(stl_path)

    except Exception as e:
        print(f"[stl_exporter] scan_{scan_id}: {e}")
        return ""
