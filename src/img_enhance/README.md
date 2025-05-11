# Image Enhancement Module for OCR

This module provides tools for enhancing images to improve OCR (Optical Character Recognition) results. It includes both automatic and manual enhancement options, with a focus on improving text readability.

## Features

- **Automatic image enhancement** with intelligent parameter selection
- **Manual enhancement** with fine control over parameters
- **Batch processing** for multiple images
- **Command-line interface** for easy integration
- **Comparison tools** to visualize enhancements
- **Parameter saving/loading** for consistent results

## Usage

### As a Python Module

```python
# Automatic enhancement
from src.img_enhance import auto_enhance_image

# Enhance an image automatically
enhanced_image = auto_enhance_image("path/to/image.jpg")
enhanced_image.save("path/to/output.jpg")

# Manual enhancement with custom parameters
from src.img_enhance import ImageEnhancer, EnhancementParams

# Create custom enhancement parameters
params = EnhancementParams(
    brightness=1.2,
    contrast=1.5,
    sharpness=1.3,
    denoise=True
)

# Create enhancer and process image
enhancer = ImageEnhancer(params)
enhanced = enhancer.enhance("path/to/image.jpg")
enhanced.save("path/to/output.jpg")

# Generate preview grid with different enhancements
from src.img_enhance.auto_enhance import get_enhancement_preview_grid

preview = get_enhancement_preview_grid("path/to/image.jpg")
preview.save("path/to/preview_grid.jpg")

# Create comparison image
from src.img_enhance.utils import create_comparison_image
from PIL import Image

original = Image.open("path/to/image.jpg")
enhanced = enhancer.enhance(original)
comparison = create_comparison_image(original, enhanced, params)
comparison.save("path/to/comparison.jpg")
```

### Command Line Interface

The module includes a command-line interface for easy use:

```bash
# Automatic enhancement
python -m src.img_enhance.cli auto input.jpg -o output.jpg

# Manual enhancement with parameters
python -m src.img_enhance.cli manual input.jpg -o output.jpg --brightness 1.2 --contrast 1.5 --sharpness 1.3 --denoise

# Batch processing
python -m src.img_enhance.cli batch input_directory/ -o output_directory/ --recursive

# Generate preview grid
python -m src.img_enhance.cli preview input.jpg -o preview_grid.jpg
```

## Enhancement Parameters

The following parameters can be adjusted:

- **brightness**: Adjust image brightness (0.5-1.5, default: 1.0)
- **contrast**: Adjust image contrast (0.5-2.0, default: 1.0)
- **sharpness**: Adjust image sharpness (0.0-2.0, default: 1.0)
- **color**: Adjust color saturation (0.0-2.0, default: 1.0)
- **denoise**: Apply denoising filter (default: False)
- **binarize**: Convert to black and white (default: False)
- **binarize_threshold**: Threshold for binarization (0-255, default: 128)
- **deskew**: Attempt to straighten text (default: False)
- **resize_factor**: Scale the image (e.g., 1.5 for 150%, default: None)

## Integration with GUI

This module is designed to be easily integrated with GUI applications. The `ImageEnhancer` class provides methods that can be connected to GUI controls, and the automatic enhancement functions can be used for one-click enhancements.

Example of GUI integration:

```python
from src.img_enhance import ImageEnhancer, EnhancementParams, auto_enhance_image

class OCRApplication:
    def __init__(self):
        self.enhancer = ImageEnhancer()
        self.current_image = None
        self.enhanced_image = None
        
    def load_image(self, path):
        self.current_image = Image.open(path)
        return self.current_image
        
    def auto_enhance(self):
        if self.current_image:
            self.enhanced_image = auto_enhance_image(self.current_image)
            return self.enhanced_image
        return None
        
    def manual_enhance(self, brightness, contrast, sharpness, denoise, binarize):
        if self.current_image:
            params = EnhancementParams(
                brightness=brightness,
                contrast=contrast,
                sharpness=sharpness,
                denoise=denoise,
                binarize=binarize
            )
            self.enhancer.set_params(params)
            self.enhanced_image = self.enhancer.enhance(self.current_image)
            return self.enhanced_image
        return None
```

## Requirements

- Python 3.6+
- Pillow (PIL)
- NumPy
- Matplotlib (for plotting metrics)

## License

MIT License 