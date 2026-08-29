# 🧠 MRI Brain Image Segmentation using Multi-Level Thresholding

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Domain](https://img.shields.io/badge/Domain-Biomedical%20Engineering-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

An end-to-end Python pipeline designed for structural brain MRI segmentation. This repository implements **Otsu’s Global Thresholding** (2-class segmentation) and **Multi-Level Quantile Division** (3-class segmentation) to isolate brain tissue types from background signals.

---

## 📌 Project Overview

Image thresholding is a foundational technique in quantitative medical imaging. This project analyzes intensity distributions in brain Magnetic Resonance Imaging (MRI) scans to segment structural tissue types.

### 🔬 Scientific Purpose
From a biomedical engineering perspective, structural MRI segmentation is a critical prerequisite for quantitative image analysis. The core objectives are: 

* **Tissue Characterization:** Isolate distinct intracranial tissue compartments, including Cerebrospinal Fluid (CSF), Gray Matter (GM), and White Matter (WM).
* **Anatomical Delineation:** Dissect cerebral structures from non-brain regions (e.g., cranial bone, background acquisition noise) to support volumetric analysis and pathological detection.
* **Variance Optimization:** Evaluate the effectiveness of variance-based intensity clustering ($\sigma_B^2$) versus parametric percentile binning for medical image segmentation.


### 💻 Computational & Engineering Purpose

This project establishes a standardized, reproducible processing pipeline:
* **Automated Data Processing:** Standardize multi-dimensional array inputs into normalized floating-point grayscale intensity matrices ($[0, 1]$ range).
* **Algorithmic Implementation:** Implement global parametric (Quantiles) and non-parametric (Otsu) thresholding algorithms without manual intervention.
* **Modular Codebase & Reproducibility:** Structure an end-to-end Python processing pipeline with automated figure generation, output logging, and version-controlled environments.


## 📂 Project Architecture

```text
mri-brain-segmentation/
├── data/
│   └── irmsansbruit.png        # Input brain MRI benchmark dataset
├── outputs/
│   ├── segmentation_results.png # Visual comparison of segmented masks
│   └── histograms_results.png   # Pixel intensity distributions & thresholds
├── .gitignore                  # Git exclusion configuration
├── main.py                     # Primary pipeline script
├── README.md                   # Project documentation
└── requirements.txt            # Dependency specs

```

---

## 🧮 Theoretical Background

### 1. Otsu's Automatic Thresholding

Otsu's algorithm searches for an optimal global threshold $t^*$ that minimizes intra-class variance, which is mathematically equivalent to maximizing the **between-class variance**:

$$\sigma_B^2(t) = \omega_0(t) \omega_1(t) \left[ \mu_0(t) - \mu_1(t) \right]^2$$

Where:

* $\omega_0(t), \omega_1(t)$ represent class probabilities separated by threshold $t$.
* $\mu_0(t), \mu_1(t)$ represent mean pixel intensities of each class.

### 2. Multi-Level Quantile Thresholding

Quantile partitioning divides continuous pixel distributions into equal population bins based on percentiles:

* **Class 0 (Dark):** Intensities $\le P_{33}$
* **Class 1 (Medium):** $P_{33} < \text{Intensities} \le P_{66}$
* **Class 2 (Bright):** Intensities $> P_{66}$

---

## 💻 Quick Start & Execution

### 1. Prerequisites & Dependencies

Ensure you have Python installed, then install project dependencies:

```cmd
pip install -r requirements.txt

```

### 2. Execution Pipeline

Run the main script from your Anaconda Prompt terminal:

```cmd
python main.py

```

---

## 📊 Pipeline Outputs

Upon successful execution, figures are saved automatically into the `outputs/` directory:

| Output Artifact | File Description |
| --- | --- |
| **`segmentation_results.png`** | Comparative grid displaying Raw Grayscale MRI, Binary Otsu Mask, and 3-Class Segmented Volume. |
| **`histograms_results.png`** | Intensity frequency distributions overlaying threshold markers ($t_{\text{Otsu}}$, $P_{33}$, $P_{66}$). |

---

## 📜 License & Citation

Distributed under the MIT License. Data provided via `scikit-image` medical image benchmark datasets (`skimage.data.brain`).

```

---