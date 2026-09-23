# 🧠 MRI Brain Image Segmentation with Thresholding

A Python mini-project exploring classical image-segmentation methods on brain MRI images.

## 🎯 Objective

The project compares two intensity-based approaches:

- **Otsu global thresholding**
- **Multi-level quantile-based intensity division**

The purpose is to understand how intensity distributions can be used to separate regions in grayscale medical images.

## 🔬 Processing

The pipeline:

1. Loads MRI images.
2. Converts and normalizes image intensities.
3. Applies Otsu thresholding.
4. Applies multi-level intensity division.
5. Visualizes the resulting segmentation masks.

## 🛠️ Technologies

Python · NumPy · OpenCV · scikit-image · Matplotlib

## ⚠️ Scope and limitations

This is an educational image-processing exercise. Thresholding alone does not provide validated anatomical tissue segmentation or clinical diagnosis.

## 🚀 Run

\`\`\`bash
pip install -r requirements.txt
python main.py
\`\`\`
