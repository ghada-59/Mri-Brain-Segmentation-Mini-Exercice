# Contour Studio — React interface

This optional React/Vite interface calls the existing classical thresholding functions in main.py through a local FastAPI adapter.

## Setup

Install Python dependencies from the repository root:

~~~bash
python -m pip install -r requirements-react-api.txt
~~~

Start the API in terminal 1:

~~~bash
python -m uvicorn segmentation_api:app --reload --host 127.0.0.1 --port 8000
~~~

In terminal 2:

~~~bash
cd frontend
npm install
npm run dev
~~~

Open the local URL printed by Vite, normally http://127.0.0.1:5173/.

## Workflow

1. Select or drag in a PNG, JPG, BMP or TIFF image.
2. Confirm that the local preview appears.
3. Run segmentation to calculate Otsu two-class and quantile three-class masks.
4. Review the thresholds, output images and grayscale histogram.

The original image is processed in memory by the local API. The interface does not save uploaded images automatically.

## Scope

This is an educational intensity-thresholding exercise. It does not perform anatomical segmentation, tumour localization, or diagnosis. Intensity regions should not be described as validated anatomical boundaries.
