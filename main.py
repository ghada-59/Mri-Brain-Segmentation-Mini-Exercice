"""Brain MRI Image Segmentation Pipeline via Thresholding.

This module loads a brain MRI slice, applies grayscale intensity normalization,
and performs 2-class (Otsu) and 3-class (Quantile) segmentations.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from skimage import color, filters, io


def load_and_preprocess_image(image_path: str) -> np.ndarray:
    """Loads an MRI image and normalizes it to a float array ranging from 0 to 1."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at location: {image_path}")

    image = io.imread(image_path)
    if image.ndim == 3:
        gray_image = color.rgb2gray(image)
    else:
        gray_image = (
            image / 255.0 if image.dtype == np.uint8 else image.astype(float)
        )
    return gray_image


def perform_segmentation(gray_image: np.ndarray):
    """Computes 2-class Otsu and 3-class quantile thresholdings."""
    # 1. Otsu Thresholding (2 classes)
    threshold_otsu = filters.threshold_otsu(gray_image)
    segmented_2class = gray_image > threshold_otsu

    # 2. Quantile Thresholding (3 classes)
    seuil1 = np.percentile(gray_image, 33)
    seuil2 = np.percentile(gray_image, 66)

    segmented_3class = np.zeros_like(gray_image, dtype=np.uint8)
    segmented_3class[(gray_image > seuil1) & (gray_image <= seuil2)] = 1
    segmented_3class[gray_image > seuil2] = 2

    return threshold_otsu, segmented_2class, seuil1, seuil2, segmented_3class


def plot_results(
    gray_image, segmented_2class, segmented_3class, t_otsu, s1, s2, output_dir
):
    """Displays and saves the segmented images and their corresponding histograms."""
    os.makedirs(output_dir, exist_ok=True)

    # 1. Display Segmented Images
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(gray_image, cmap="gray")
    axes[0].set_title("Original Grayscale MRI")
    axes[0].axis("off")

    axes[1].imshow(segmented_2class, cmap="gray")
    axes[1].set_title(f"2-Class Segmentation\n(Otsu = {t_otsu:.3f})")
    axes[1].axis("off")

    axes[2].imshow(segmented_3class, cmap="viridis")
    axes[2].set_title(f"3-Class Segmentation\n(Thresholds = {s1:.3f}, {s2:.3f})")
    axes[2].axis("off")

    plt.tight_layout()
    fig.savefig(
        os.path.join(output_dir, "segmentation_results.png"), dpi=300
    )
    plt.show()

    # 2. Display Intensity Histograms with Threshold Lines
    fig_hist, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.hist(gray_image.ravel(), bins=50, color="skyblue", ec="black", alpha=0.7)
    ax1.axvline(
        t_otsu, color="red", linestyle="--", label=f"Otsu Threshold: {t_otsu:.3f}"
    )
    ax1.set_title("Histogram - 2 Classes")
    ax1.set_xlabel("Grayscale Intensity")
    ax1.set_ylabel("Frequency")
    ax1.legend()

    ax2.hist(gray_image.ravel(), bins=50, color="skyblue", ec="black", alpha=0.7)
    ax2.axvline(s1, color="red", linestyle="--", label=f"Threshold 1: {s1:.3f}")
    ax2.axvline(s2, color="green", linestyle="--", label=f"Threshold 2: {s2:.3f}")
    ax2.set_title("Histogram - 3 Classes")
    ax2.set_xlabel("Grayscale Intensity")
    ax2.set_ylabel("Frequency")
    ax2.legend()

    plt.tight_layout()
    fig_hist.savefig(
        os.path.join(output_dir, "histograms_results.png"), dpi=300
    )
    plt.show()


def main():
    img_path = os.path.join("data", "irmsansbruit.png")
    output_dir = "outputs"

    print("[INFO] Loading and preprocessing MRI scan...")
    gray_img = load_and_preprocess_image(img_path)

    print("[INFO] Computing threshold segmentations...")
    t_otsu, seg2, s1, s2, seg3 = perform_segmentation(gray_img)

    print(f"[RESULTS] Otsu Threshold (2 classes): {t_otsu:.3f}")
    print(f"[RESULTS] Quantile Thresholds (3 classes): {s1:.3f}, {s2:.3f}")

    print("[INFO] Generating and saving figure plots...")
    plot_results(gray_img, seg2, seg3, t_otsu, s1, s2, output_dir)
    print("[INFO] Pipeline executed successfully! Output figures saved in 'outputs/'.")


if __name__ == "__main__":
    main()