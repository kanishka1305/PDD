import numpy as np


def normalize_volume(volume):

    volume = volume.astype(np.float32)

    volume = (volume - volume.min()) / (
        volume.max() - volume.min()
    )

    return volume


def resize_volume(volume):

    return volume