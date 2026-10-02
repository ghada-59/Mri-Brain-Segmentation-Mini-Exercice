# Contributing to MRI Brain Segmentation

Thanks for helping improve this image-processing project.

## Setup

```bash
git clone https://github.com/ghada-59/Mri-Brain-Segmentation-Mini-Exercice.git
cd Mri-Brain-Segmentation-Mini-Exercice
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Scope

This project implements a small MRI thresholding pipeline using:
- grayscale normalization,
- Otsu thresholding,
- multi-level quantile segmentation,
- result plotting and output generation.

## Standards

- Keep preprocessing logic separate from visualization code.
- Use explicit function names and docstrings.
- Prefer reproducible pipeline steps over hard-coded one-off operations.
- Document assumptions about the image input.

## Validation

Run the pipeline before submitting a patch:

```bash
python main.py
```

Check that the files in `outputs/` are generated and the segmentation figures are still readable.

## Pull request workflow

1. Create a branch for your fix/feature.
2. Keep changes focused and reproducible.
3. Validate the output locally.
4. Submit a pull request with a short summary.

## License

By contributing, you agree that your work will be distributed under the MIT License.
