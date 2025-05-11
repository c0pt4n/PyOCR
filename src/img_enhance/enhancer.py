from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any, Union
import os

@dataclass
class EnhancementParams:
    """Parameters for image enhancement"""
    brightness: float = 1.0  # 0.5 to 1.5
    contrast: float = 1.0    # 0.5 to 2.0
    sharpness: float = 1.0   # 0.0 to 2.0
    color: float = 1.0       # 0.0 to 2.0
    denoise: bool = False
    binarize: bool = False
    binarize_threshold: int = 128  # 0 to 255
    deskew: bool = False
    resize_factor: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert parameters to dictionary"""
        return {
            "brightness": self.brightness,
            "contrast": self.contrast,
            "sharpness": self.sharpness,
            "color": self.color,
            "denoise": self.denoise, 
            "binarize": self.binarize,
            "binarize_threshold": self.binarize_threshold,
            "deskew": self.deskew,
            "resize_factor": self.resize_factor
        }
    
    @classmethod
    def from_dict(cls, params_dict: Dict[str, Any]) -> 'EnhancementParams':
        """Create parameters from dictionary"""
        return cls(**params_dict)


class ImageEnhancer:
    """Class for enhancing images for OCR processing"""
    
    def __init__(self, params: Optional[EnhancementParams] = None):
        """Initialize with enhancement parameters"""
        self.params = params or EnhancementParams()
        
    def set_params(self, params: EnhancementParams) -> None:
        """Update enhancement parameters"""
        self.params = params
        
    def update_params(self, **kwargs) -> None:
        """Update specific parameters"""
        for key, value in kwargs.items():
            if hasattr(self.params, key):
                setattr(self.params, key, value)
    
    def enhance(self, image: Union[str, Image.Image]) -> Image.Image:
        """
        Enhance the image using current parameters
        
        Args:
            image: PIL Image or path to image file
            
        Returns:
            Enhanced PIL Image
        """
        # Load image if path is provided
        if isinstance(image, str):
            if not os.path.exists(image):
                raise FileNotFoundError(f"Image file not found: {image}")
            img = Image.open(image).convert('RGB')
        else:
            img = image
            
        # Apply enhancements in sequence
        enhanced = self._apply_enhancements(img)
        
        return enhanced
    
    def _apply_enhancements(self, img: Image.Image) -> Image.Image:
        """Apply all enhancements based on parameters"""
        # Make a copy to avoid modifying the original
        result = img.copy()
        
        # Apply resize if specified
        if self.params.resize_factor is not None and self.params.resize_factor > 0:
            new_width = int(result.width * self.params.resize_factor)
            new_height = int(result.height * self.params.resize_factor)
            result = result.resize((new_width, new_height), Image.LANCZOS)
        
        # Apply basic enhancements
        if self.params.brightness != 1.0:
            result = ImageEnhance.Brightness(result).enhance(self.params.brightness)
            
        if self.params.contrast != 1.0:
            result = ImageEnhance.Contrast(result).enhance(self.params.contrast)
            
        if self.params.color != 1.0:
            result = ImageEnhance.Color(result).enhance(self.params.color)
            
        if self.params.sharpness != 1.0:
            result = ImageEnhance.Sharpness(result).enhance(self.params.sharpness)
        
        # Apply denoising if enabled
        if self.params.denoise:
            result = result.filter(ImageFilter.MedianFilter(size=3))
        
        # Apply deskewing if enabled
        if self.params.deskew:
            result = self._deskew_image(result)
            
        # Apply binarization if enabled
        if self.params.binarize:
            result = self._binarize_image(result, self.params.binarize_threshold)
            
        return result
    
    def _binarize_image(self, img: Image.Image, threshold: int = 128) -> Image.Image:
        """Convert image to binary (black and white)"""
        # Convert to grayscale
        gray = img.convert('L')
        
        # Apply threshold
        return gray.point(lambda x: 0 if x < threshold else 255, '1')
    
    def _deskew_image(self, img: Image.Image) -> Image.Image:
        """
        Basic deskewing implementation using Pillow
        For more advanced deskewing, consider using OpenCV
        """
        # For now, just returning the image as-is
        # A proper implementation would calculate skew angle and rotate
        return img
    
    def save_enhanced_image(self, image: Union[str, Image.Image], output_path: str) -> None:
        """
        Enhance and save image
        
        Args:
            image: PIL Image or path to image file
            output_path: Path to save enhanced image
        """
        enhanced = self.enhance(image)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # Save the enhanced image
        enhanced.save(output_path)
        
    def get_preview(self, image: Union[str, Image.Image], size: Tuple[int, int] = (400, 400)) -> Image.Image:
        """
        Generate a preview of enhanced image
        
        Args:
            image: PIL Image or path to image file
            size: Size of preview image (width, height)
            
        Returns:
            Preview image resized to specified dimensions
        """
        enhanced = self.enhance(image)
        
        # Resize for preview
        preview = enhanced.copy()
        preview.thumbnail(size, Image.LANCZOS)
        
        return preview
    
    def compare_original_enhanced(self, image: Union[str, Image.Image]) -> Tuple[Image.Image, Image.Image]:
        """
        Return both original and enhanced images for comparison
        
        Args:
            image: PIL Image or path to image file
            
        Returns:
            Tuple of (original_image, enhanced_image)
        """
        # Load image if path is provided
        if isinstance(image, str):
            if not os.path.exists(image):
                raise FileNotFoundError(f"Image file not found: {image}")
            original = Image.open(image).convert('RGB')
        else:
            original = image.copy()
            
        enhanced = self.enhance(original)
        
        return original, enhanced 