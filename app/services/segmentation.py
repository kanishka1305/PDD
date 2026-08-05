import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# THRESHOLD SEGMENTATION
# ─────────────────────────────────────────────────────────────────────────────

def run_segmentation(volume: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """
    Binary-threshold segmentation.
    Falls back to progressively lower thresholds so single-slice / sparse
    DICOM files still yield a usable mask.
    """
    for t in [threshold, 0.4, 0.3, 0.2, 0.1, 0.05]:
        mask = (volume > t).astype(np.uint8)
        if np.sum(mask) >= 100:
            return mask
    # Last resort — return everything non-zero
    return (volume > 0).astype(np.uint8)


# ─────────────────────────────────────────────────────────────────────────────
# 7-REGION MANDIBLE PARTITION
#
#  Works on ANY volume shape including single-slice (Z=1) DICOMs.
#
#  For single-slice scans the Z dimension is collapsed and the 2D image is
#  partitioned purely in X (left/right) and Y (anterior/posterior):
#
#   Superior Y region  → condylar heads (outer X) + coronoids (inner X)
#   Mid Y region       → angle + ramus
#   Inferior Y region  → body (outer X) + symphyseal (centre X)
#
# ─────────────────────────────────────────────────────────────────────────────

def partition_mandible_7_regions(mask: np.ndarray) -> dict:
    """
    Returns a dict of 9 uint8 arrays (same shape as mask).
    Keys: condylar_head_L/R, coronoid_L/R, angle_ramus_L/R,
          body_L/R, symphyseal_parasymphyseal
    """
    region_keys = [
        "condylar_head_L", "condylar_head_R",
        "coronoid_L",      "coronoid_R",
        "angle_ramus_L",   "angle_ramus_R",
        "body_L",          "body_R",
        "symphyseal_parasymphyseal",
    ]
    regions = {k: np.zeros_like(mask) for k in region_keys}

    active = np.argwhere(mask)
    if len(active) == 0:
        return regions

    z_min, y_min, x_min = active.min(axis=0)
    z_max, y_max, x_max = active.max(axis=0)

    z_range = z_max - z_min
    y_range = max(y_max - y_min, 1)
    x_range = max(x_max - x_min, 1)

    # ── X midpoints ──────────────────────────────────────────────────────────
    x_mid     = int(x_min + 0.50 * x_range)
    x_inner_L = int(x_min + 0.35 * x_range)   # condyle_L | coronoid_L
    x_inner_R = int(x_min + 0.65 * x_range)   # coronoid_R | condyle_R
    x_body_L  = int(x_min + 0.35 * x_range)
    x_body_R  = int(x_min + 0.65 * x_range)

    # ─────────────────────────────────────────────────────────────────────────
    # CASE A: proper 3-D volume (z_range >= 2)
    # Partition primarily along Z (superior → inferior)
    # ─────────────────────────────────────────────────────────────────────────
    if z_range >= 2:
        z_cond_end  = int(z_min + 0.25 * z_range)
        z_ramus_end = int(z_min + 0.55 * z_range)

        # Superior slice range
        zs = np.s_[z_min : z_cond_end + 1]
        regions["condylar_head_L"][zs, :, x_min      : x_inner_L]  = mask[zs, :, x_min      : x_inner_L]
        regions["condylar_head_R"][zs, :, x_inner_R  : x_max + 1]  = mask[zs, :, x_inner_R  : x_max + 1]
        regions["coronoid_L"]     [zs, :, x_inner_L  : x_mid]      = mask[zs, :, x_inner_L  : x_mid]
        regions["coronoid_R"]     [zs, :, x_mid       : x_inner_R]  = mask[zs, :, x_mid      : x_inner_R]

        # Mid slice range
        zm = np.s_[z_cond_end + 1 : z_ramus_end + 1]
        regions["angle_ramus_L"][zm, :, x_min : x_mid]      = mask[zm, :, x_min : x_mid]
        regions["angle_ramus_R"][zm, :, x_mid : x_max + 1]  = mask[zm, :, x_mid : x_max + 1]

        # Inferior slice range
        zi = np.s_[z_ramus_end + 1 : z_max + 1]
        regions["body_L"]                    [zi, :, x_min   : x_body_L]  = mask[zi, :, x_min   : x_body_L]
        regions["body_R"]                    [zi, :, x_body_R: x_max + 1] = mask[zi, :, x_body_R: x_max + 1]
        regions["symphyseal_parasymphyseal"] [zi, :, x_body_L: x_body_R]  = mask[zi, :, x_body_L: x_body_R]

    # ─────────────────────────────────────────────────────────────────────────
    # CASE B: 2-D / single-slice (z_range == 0 or 1)
    # Partition by Y (rows) instead of Z
    # Top 25% Y → condylar + coronoid zone
    # Mid 25-55% Y → angle + ramus zone
    # Bottom 45% Y → body + symphyseal zone
    # ─────────────────────────────────────────────────────────────────────────
    else:
        y_cond_end  = int(y_min + 0.25 * y_range)
        y_ramus_end = int(y_min + 0.55 * y_range)

        # Superior Y band (condylar + coronoid)
        ys = np.s_[:, y_min : y_cond_end + 1, :]
        regions["condylar_head_L"][ys[0], ys[1], x_min      : x_inner_L]  = mask[ys[0], ys[1], x_min      : x_inner_L]
        regions["condylar_head_R"][ys[0], ys[1], x_inner_R  : x_max + 1]  = mask[ys[0], ys[1], x_inner_R  : x_max + 1]
        regions["coronoid_L"]     [ys[0], ys[1], x_inner_L  : x_mid]      = mask[ys[0], ys[1], x_inner_L  : x_mid]
        regions["coronoid_R"]     [ys[0], ys[1], x_mid       : x_inner_R]  = mask[ys[0], ys[1], x_mid      : x_inner_R]

        # Mid Y band (ramus)
        ym = np.s_[:, y_cond_end + 1 : y_ramus_end + 1, :]
        regions["angle_ramus_L"][ym[0], ym[1], x_min : x_mid]      = mask[ym[0], ym[1], x_min : x_mid]
        regions["angle_ramus_R"][ym[0], ym[1], x_mid : x_max + 1]  = mask[ym[0], ym[1], x_mid : x_max + 1]

        # Inferior Y band (body + symphyseal)
        yi = np.s_[:, y_ramus_end + 1 : y_max + 1, :]
        regions["body_L"]                    [yi[0], yi[1], x_min   : x_body_L]  = mask[yi[0], yi[1], x_min   : x_body_L]
        regions["body_R"]                    [yi[0], yi[1], x_body_R: x_max + 1] = mask[yi[0], yi[1], x_body_R: x_max + 1]
        regions["symphyseal_parasymphyseal"] [yi[0], yi[1], x_body_L: x_body_R]  = mask[yi[0], yi[1], x_body_L: x_body_R]

    return regions


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC WRAPPERS
# ─────────────────────────────────────────────────────────────────────────────

def run_full_segmentation(volume: np.ndarray):
    """Returns (full_mask, regions_dict)."""
    mask    = run_segmentation(volume)
    regions = partition_mandible_7_regions(mask)
    return mask, regions


def partition_mandible_mask(mask):
    """Legacy 4-region wrapper."""
    r             = partition_mandible_7_regions(mask)
    condyles      = np.clip(r["condylar_head_L"] + r["condylar_head_R"], 0, 1).astype(np.uint8)
    ramus         = np.clip(r["angle_ramus_L"]   + r["angle_ramus_R"],   0, 1).astype(np.uint8)
    parasymphysis = np.clip(r["body_L"]          + r["body_R"],          0, 1).astype(np.uint8)
    symphysis     = r["symphyseal_parasymphyseal"]
    return condyles, ramus, parasymphysis, symphysis


def run_subregional_segmentation(volume):
    """Legacy 5-return wrapper."""
    mask, regions = run_full_segmentation(volume)
    condyles      = np.clip(regions["condylar_head_L"] + regions["condylar_head_R"], 0, 1).astype(np.uint8)
    ramus         = np.clip(regions["angle_ramus_L"]   + regions["angle_ramus_R"],   0, 1).astype(np.uint8)
    parasymphysis = np.clip(regions["body_L"]          + regions["body_R"],          0, 1).astype(np.uint8)
    symphysis     = regions["symphyseal_parasymphyseal"]
    return mask, condyles, ramus, parasymphysis, symphysis
