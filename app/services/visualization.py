import matplotlib.pyplot as plt
from pathlib import Path

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


def save_segmentation_image(mask, scan_id):

    middle_slice = mask.shape[0] // 2

    image_path = RESULTS_DIR / f"segmentation_{scan_id}.png"

    plt.imshow(mask[middle_slice], cmap="gray")
    plt.axis("off")

    plt.savefig(
        image_path,
        bbox_inches="tight",
        pad_inches=0
    )

    plt.close()

    return str(image_path)