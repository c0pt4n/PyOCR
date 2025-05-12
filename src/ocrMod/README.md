# OCR Module

This module provides an interface to the Tesseract OCR engine for text extraction from images.

## Features

- Extract text from images using Tesseract OCR
- Support for multiple output formats:
  - Plain text
  - hOCR (HTML)
  - PDF
  - TSV
  - ALTO XML
  - PAGE
- Cross-platform compatibility
- Configurable OCR parameters

## Usage

```python
from src.ocrMod.ocr_engine import OCREngine

# Initialize the OCR engine
ocr = OCREngine()

# Process an image with default settings (English language, text output)
text = ocr.process_image("path/to/image.jpg")

# Process with custom settings
result = ocr.process_image(
    image_path="path/to/image.jpg",
    lang="eng+fra",  # English and French
    output_format="hocr",  # hOCR HTML output
    config="--psm 6"  # Page segmentation mode 6 (assume single uniform block of text)
)
```

## Requirements

- Python 3.6+
- Tesseract OCR (v4.0+ recommended)
- pytesseract
- Pillow (PIL Fork)

## Testing

Tests are available in the `tests/ocrMod` directory and can be run with pytest. 