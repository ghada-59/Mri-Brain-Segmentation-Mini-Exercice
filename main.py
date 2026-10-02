"""Brain MRI image segmentation with classical thresholding methods."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from skimage import color, filters, io


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_IMAGE_PATH = PROJECT_ROOT / "data" / "irmsansbruit.png"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs"


def load_and_preprocess_image(image_path):
    """Load an MRI image and normalize its grayscale intensity to [0, 1]."""
    image_path = Path(image_path)
    if not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = io.imread(image_path)

    if image.ndim == 3:
        if image.shape[2] == 4:
            image = image[..., :3]
        if image.shape[2] != 3:
            raise ValueError(f"Unsupported channel count: {image.shape[2]}")
        gray_image = color.rgb2gray(image)
    elif image.ndim == 2:
        gray_image = image.astype(np.float32)
        min_value = float(np.min(gray_image))
        max_value = float(np.max(gray_image))
        if max_value <= min_value:
            raise ValueError("The grayscale image has no intensity variation.")
        gray_image = (gray_image - min_value) / (max_value - min_value)
    else:
        raise ValueError(f"Unsupported image shape: {image.shape}")

    return np.asarray(gray_image, dtype=np.float32)


def perform_segmentation(gray_image):
    """Compute 2-class Otsu and 3-class quantile segmentations."""
    gray_image = np.asarray(gray_image)
    if gray_image.ndim != 2:
        raise ValueError("gray_image must be a 2D grayscale image.")
    if not np.isfinite(gray_image).all():
        raise ValueError("gray_image contains NaN or infinite values.")

    threshold_otsu = filters.threshold_otsu(gray_image)
    segmented_2class = gray_image > threshold_otsu

    threshold_1, threshold_2 = np.percentile(gray_image, [33, 66])
    segmented_3class = np.zeros_like(gray_image, dtype=np.uint8)
    segmented_3class[gray_image > threshold_1] = 1
    segmented_3class[gray_image > threshold_2] = 2

    return (
        threshold_otsu,
        segmented_2class,
        threshold_1,
        threshold_2,
        segmented_3class,
    )


def plot_results(
    gray_image,
    segmented_2class,
    segmented_3class,
    threshold_otsu,
    threshold_1,
    threshold_2,
    output_dir,
):
    """Save segmentation and histogram figures without requiring a GUI."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    figure, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(gray_image, cmap="gray")
    axes[0].set_title("Original Grayscale MRI")
    axes[0].axis("off")

    axes[1].imshow(segmented_2class, cmap="gray")
    axes[1].set_title(f"2-Class Segmentation\n(Otsu = {threshold_otsu:.3f})")
    axes[1].axis("off")

    axes[2].imshow(segmented_3class, cmap="viridis")
    axes[2].set_title(
        f"3-Class Segmentation\n"
        f"(Thresholds = {threshold_1:.3f}, {threshold_2:.3f})"
    )
    axes[2].axis("off")

    figure.tight_layout()
    figure.savefig(output_dir / "segmentation_results.png", dpi=300)
    plt.close(figure)

    figure_hist, axes_hist = plt.subplots(1, 2, figsize=(12, 4))
    axes_hist[0].hist(gray_image.ravel(), bins=50)
    axes_hist[0].axvline(
        threshold_otsu,
        linestyle="--",
        label=f"Otsu: {threshold_otsu:.3f}",
    )
    axes_hist[0].set_title("Histogram - 2 Classes")
    axes_hist[0].set_xlabel("Grayscale Intensity")
    axes_hist[0].set_ylabel("Frequency")
    axes_hist[0].legend()

    axes_hist[1].hist(gray_image.ravel(), bins=50)
    axes_hist[1].axvline(
        threshold_1,
        linestyle="--",
        label=f"Threshold 1: {threshold_1:.3f}",
    )
    axes_hist[1].axvline(
        threshold_2,
        linestyle="--",
        label=f"Threshold 2: {threshold_2:.3f}",
    )
    axes_hist[1].set_title("Histogram - 3 Classes")
    axes_hist[1].set_xlabel("Grayscale Intensity")
    axes_hist[1].set_ylabel("Frequency")
    axes_hist[1].legend()

    figure_hist.tight_layout()
    figure_hist.savefig(output_dir / "histograms_results.png", dpi=300)
    plt.close(figure_hist)


def main():
    print("[INFO] Loading and preprocessing MRI scan...")
    gray_img = load_and_preprocess_image(DEFAULT_IMAGE_PATH)

    print("[INFO] Computing threshold segmentations...")
    threshold_otsu, seg2, threshold_1, threshold_2, seg3 = perform_segmentation(
        gray_img
    )

    print(f"[RESULTS] Otsu threshold: {threshold_otsu:.3f}")
    print(f"[RESULTS] Quantile thresholds: {threshold_1:.3f}, {threshold_2:.3f}")

    print("[INFO] Generating and saving figures...")
    plot_results(
        gray_img,
        seg2,
        seg3,
        threshold_otsu,
        threshold_1,
        threshold_2,
        DEFAULT_OUTPUT_DIR,
    )
    print(f"[INFO] Figures saved in: {DEFAULT_OUTPUT_DIR}")


if __name__ == "__main__":
    main()
