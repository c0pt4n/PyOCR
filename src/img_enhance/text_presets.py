from PIL import Image
from typing import Union, Dict
from .enhancer import ImageEnhancer, EnhancementParams

def mixed_content_text_enhance(image: Union[str, Image.Image]) -> Image.Image:
    """
    Enhance images with mixed content while preserving text readability
    
    Args:
        image: PIL Image or path to image file
        
    Returns:
        Enhanced PIL Image with clear, readable text
    """
    # Create parameters focused on text clarity without destroying other content
    params = EnhancementParams(
        brightness=1.05,      # Very slight brightness increase 
        contrast=1.2,         # Moderate contrast increase
        sharpness=1.3,        # Moderate sharpening
        color=0.9,            # Slightly reduce color to emphasize text
        denoise=True,         # Remove noise
        binarize=False,       # Don't binarize as it ruins mixed content
        deskew=False          # Don't automatically deskew
    )
    
    # Create enhancer and apply parameters
    enhancer = ImageEnhancer(params)
    return enhancer.enhance(image)

def text_document_enhance(image: Union[str, Image.Image]) -> Image.Image:
    """
    Enhance specifically for text document clarity - optimized for OCR
    
    Args:
        image: PIL Image or path to image file
        
    Returns:
        Enhanced PIL Image optimized for text clarity
    """
    # Create parameters focused on text clarity
    params = EnhancementParams(
        brightness=1.05,      # Slight brightness increase
        contrast=1.15,        # Modest contrast increase
        sharpness=1.2,        # Modest sharpening
        color=0.8,            # Slightly reduce color to make text stand out
        denoise=True,         # Remove noise
        binarize=False,       # Don't binarize by default as it can destroy information
        deskew=False          # Don't automatically deskew
    )
    
    # Create enhancer and apply parameters
    enhancer = ImageEnhancer(params)
    return enhancer.enhance(image)

def text_only_enhance(image: Union[str, Image.Image]) -> Image.Image:
    """
    Enhance specifically for pure text content - maximizes contrast for OCR
    
    Args:
        image: PIL Image or path to image file
        
    Returns:
        Enhanced PIL Image optimized for pure text recognition
    """
    # Create parameters focused on maximum text contrast
    params = EnhancementParams(
        brightness=1.0,       # Neutral brightness
        contrast=1.3,         # Moderate contrast
        sharpness=1.2,        # Moderate sharpness
        color=0.7,            # Reduce color saturation to emphasize text
        denoise=True,         # Remove noise
        binarize=False,       # Don't binarize automatically
        deskew=False          # Don't automatically deskew
    )
    
    # Create enhancer and apply parameters
    enhancer = ImageEnhancer(params)
    return enhancer.enhance(image)

def receipt_enhance(image: Union[str, Image.Image]) -> Image.Image:
    """
    Enhance specifically for receipts and low-contrast thermal paper
    
    Args:
        image: PIL Image or path to image file
        
    Returns:
        Enhanced PIL Image optimized for receipt processing
    """
    # Create parameters focused on receipt enhancement
    params = EnhancementParams(
        brightness=1.1,       # Increase brightness for faded receipts
        contrast=1.4,         # Moderate-high contrast
        sharpness=1.2,        # Moderate sharpening
        color=0.0,            # Remove color (receipts are generally grayscale)
        denoise=True,         # Remove noise
        binarize=False,       # Don't binarize automatically
        deskew=False          # Don't automatically deskew
    )
    
    # Create enhancer and apply parameters
    enhancer = ImageEnhancer(params)
    return enhancer.enhance(image)

def get_preset_name(preset_id: int) -> str:
    """Get the name of a preset by its ID"""
    presets = {
        0: "Mixed Content with Text Enhancement",
        1: "Document Text Enhancement",
        2: "Pure Text Enhancement",
        3: "Receipt Text Enhancement",
    }
    return presets.get(preset_id, "Unknown Preset")

def enhance_with_preset(image: Union[str, Image.Image], preset_id: int) -> Image.Image:
    """
    Enhance an image using a predefined preset
    
    Args:
        image: PIL Image or path to image file
        preset_id: Preset identifier (0-3)
        
    Returns:
        Enhanced PIL Image
    """
    presets = {
        0: mixed_content_text_enhance,
        1: text_document_enhance,
        2: text_only_enhance,
        3: receipt_enhance,
    }
    
    if preset_id in presets:
        return presets[preset_id](image)
    else:
        # Default to mixed content enhancement
        return mixed_content_text_enhance(image) 