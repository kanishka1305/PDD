import numpy as np


def calculate_voxel_count(mask):

    return int(np.sum(mask))


def calculate_volume(mask, voxel_size=1.0):

    voxel_count = np.sum(mask)

    return float(voxel_count * voxel_size)