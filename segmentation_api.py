"""FastAPI adapter for the educational brain MRI thresholding exercise."""
from __future__ import annotations

import base64
import io

import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from skimage import color, io as skio

from main import perform_segmentation

app = FastAPI(title="Contour Studio API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def _data_url(array: np.ndarray, palette: str = "gray") -> str:
    values = np.asarray(array)
    if palette == "labels":
        lut = np.asarray([[34, 43, 58], [56, 160, 145], [222, 133, 157]], dtype=np.uint8)
        rgb = lut[np.clip(values.astype(np.int32), 0, 2)]
        image = Image.fromarray(rgb, "RGB")
    elif values.dtype == bool:
        image = Image.fromarray(values.astype(np.uint8) * 255, "L")
    else:
        scaled = np.clip(values, 0, 1)
        image = Image.fromarray((scaled * 255).round().astype(np.uint8), "L")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Contour Studio API"}


@app.post("/api/segment")
async def segment(file: UploadFile = File(...)):
    name = file.filename or "uploaded-mri"
    if not name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff")):
        raise HTTPException(status_code=415, detail="Upload a PNG, JPG, BMP or TIFF image.")
    try:
        raw = await file.read()
        image = skio.imread(io.BytesIO(raw))
        if image.ndim == 3:
            if image.shape[-1] == 4:
                image = image[..., :3]
            if image.shape[-1] != 3:
                raise ValueError("Expected an RGB or grayscale image.")
            gray = color.rgb2gray(image)
        elif image.ndim == 2:
            gray = image.astype(np.float32)
            low, high = float(np.min(gray)), float(np.max(gray))
            if high <= low:
                raise ValueError("The grayscale image has no intensity variation.")
            gray = (gray - low) / (high - low)
        else:
            raise ValueError("Unsupported image dimensions.")
        gray = np.asarray(gray, dtype=np.float32)
        if not np.isfinite(gray).all():
            raise ValueError("The image contains invalid pixel values.")
        threshold, seg2, q1, q2, seg3 = perform_segmentation(gray)
        histogram, edges = np.histogram(gray, bins=32, range=(0, 1))
        return {
            "filename": name,
            "width": int(gray.shape[1]),
            "height": int(gray.shape[0]),
            "otsu_threshold": float(threshold),
            "quantile_thresholds": [float(q1), float(q2)],
            "original": _data_url(gray),
            "two_class": _data_url(seg2),
            "three_class": _data_url(seg3, "labels"),
            "histogram": histogram.tolist(),
            "histogram_edges": edges.tolist(),
            "class_fractions": {
                "dark": float(np.mean(seg3 == 0)),
                "mid": float(np.mean(seg3 == 1)),
                "bright": float(np.mean(seg3 == 2)),
            },
            "note": "Intensity-based segmentation demonstration. Regions are not anatomical tumour boundaries and are not diagnostic.",
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not process the uploaded image: " + str(exc)) from exc
