# 🧠 MRI Brain Image Segmentation with Thresholding

A small academic/practice project exploring classical intensity-based image segmentation on a grayscale brain MRI image.

## 🎯 Objective

The project compares two simple thresholding strategies:

- **Otsu global thresholding** for a binary segmentation
- **33rd/66th percentile thresholds** for a three-level intensity partition

The goal is to understand how image-intensity distributions can be used to create basic segmentation masks.

## 🔬 Processing Pipeline

1. Load an MRI image from `data/irmsansbruit.png`.
2. Convert RGB/RGBA input to grayscale when necessary.
3. Normalize grayscale intensities to `[0, 1]`.
4. Compute an Otsu threshold and create a binary mask.
5. Compute the 33rd and 66th intensity percentiles and create a three-level mask.
6. Save the segmentation and histogram figures to `outputs/`.

## 🛠️ Technologies

Python · NumPy · scikit-image · Matplotlib

## 🚀 Run

Create a virtual environment and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Then run:

```bash
python main.py
```

The generated figures are saved as:

- `outputs/segmentation_results.png`
- `outputs/histograms_results.png`

## 📁 Expected Structure

```text
Mri-Brain-Segmentation-Mini-Exercice/
├── data/
│   └── irmsansbruit.png
├── main.py
├── requirements.txt
├── outputs/
├── README.md
└── .gitignore
```

## ⚠️ Limitations

- This is an **educational image-processing exercise**, not a medical diagnostic or clinical segmentation system.
- Otsu and percentile thresholding are intensity-based methods; they do not guarantee anatomically meaningful brain-tissue segmentation.
- The three-level method uses fixed image-intensity percentiles rather than learned anatomical classes.
- No ground-truth mask or segmentation-quality metric such as Dice or IoU is used in the current version.
- Results depend on the selected MRI image and its intensity distribution.

## 📝 Project Type

**Academic / practice project.** The project demonstrates basic medical-image preprocessing, thresholding and visualization without claiming clinical validity.