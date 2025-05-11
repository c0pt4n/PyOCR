from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Tuple, Dict, Any, Union, Optional
import json
from .enhancer import EnhancementParams
import matplotlib.pyplot as plt
import numpy as np

def save_params_to_json(params: EnhancementParams, output_path: str) -> None:
    """
    Save enhancement parameters to JSON file
    
    Args:
        params: EnhancementParams object
        output_path: Path to save JSON file
    """
    # Convert parameters to dictionary
    params_dict = params.to_dict()
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Save as JSON
    with open(output_path, 'w') as f:
        json.dump(params_dict, f, indent=4)

def load_params_from_json(input_path: str) -> EnhancementParams:
    """
    Load enhancement parameters from JSON file
    
    Args:
        input_path: Path to JSON file
        
    Returns:
        EnhancementParams object
    """
    # Load JSON file
    with open(input_path, 'r') as f:
        params_dict = json.load(f)
    
    # Create EnhancementParams object
    return EnhancementParams.from_dict(params_dict)

def create_comparison_image(original: Image.Image, 
                           enhanced: Image.Image, 
                           params: Optional[EnhancementParams] = None,
                           title: str = "Image Enhancement Comparison") -> Image.Image:
    """
    Create a side-by-side comparison of original and enhanced images
    
    Args:
        original: Original PIL Image
        enhanced: Enhanced PIL Image
        params: Optional EnhancementParams to display
        title: Title for the comparison image
        
    Returns:
        PIL Image with side-by-side comparison
    """
    # Ensure the same size for both images
    if original.size != enhanced.size:
        # Resize to the smaller of the two
        width = min(original.width, enhanced.width)
        height = min(original.height, enhanced.height)
        original = original.resize((width, height), Image.LANCZOS)
        enhanced = enhanced.resize((width, height), Image.LANCZOS)
    
    # Create a new image with enough space for both images and title/parameters
    margin = 20
    title_height = 40
    params_height = 120 if params else 0
    
    new_width = original.width * 2 + margin * 3
    new_height = original.height + margin * 2 + title_height + params_height
    
    comparison = Image.new('RGB', (new_width, new_height), color=(240, 240, 240))
    
    # Paste original image
    comparison.paste(original, (margin, margin + title_height))
    
    # Paste enhanced image
    comparison.paste(enhanced, (original.width + margin * 2, margin + title_height))
    
    # Add title and labels
    draw = ImageDraw.Draw(comparison)
    
    # Try to use a nice font, fall back to default if not available
    try:
        font_title = ImageFont.truetype("Arial", 20)
        font_text = ImageFont.truetype("Arial", 12)
    except IOError:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
    
    # Draw title
    draw.text((new_width // 2, margin // 2), title, fill=(0, 0, 0), font=font_title, anchor="mm")
    
    # Draw labels
    draw.text((margin + original.width // 2, margin + title_height - 10), 
              "Original", fill=(0, 0, 0), font=font_text, anchor="mm")
    
    draw.text((margin * 2 + original.width + enhanced.width // 2, margin + title_height - 10), 
              "Enhanced", fill=(0, 0, 0), font=font_text, anchor="mm")
    
    # Add parameters if provided
    if params:
        y_pos = margin + title_height + original.height + 10
        
        param_text = [
            f"Brightness: {params.brightness:.2f}",
            f"Contrast: {params.contrast:.2f}",
            f"Sharpness: {params.sharpness:.2f}",
            f"Color: {params.color:.2f}",
            f"Denoise: {'Yes' if params.denoise else 'No'}",
            f"Binarize: {'Yes' if params.binarize else 'No'}"
        ]
        
        if params.binarize:
            param_text.append(f"Binarize Threshold: {params.binarize_threshold}")
        
        if params.deskew:
            param_text.append(f"Deskew: Yes")
        
        if params.resize_factor is not None:
            param_text.append(f"Resize Factor: {params.resize_factor:.2f}x")
        
        # Draw parameter values
        for i, text in enumerate(param_text):
            draw.text((margin, y_pos + i * 20), text, fill=(0, 0, 0), font=font_text)
    
    return comparison

def plot_enhancement_metrics(original_image: Union[str, Image.Image], 
                            enhanced_image: Union[str, Image.Image],
                            params: EnhancementParams,
                            show_plot: bool = True,
                            save_path: Optional[str] = None) -> None:
    """
    Plot metrics showing the before/after enhancement effects
    
    Args:
        original_image: Original image path or PIL Image
        enhanced_image: Enhanced image path or PIL Image
        params: Enhancement parameters used
        show_plot: Whether to display the plot
        save_path: Optional path to save the plot
    """
    # Load images if paths are provided
    if isinstance(original_image, str):
        original = Image.open(original_image).convert('RGB')
    else:
        original = original_image
        
    if isinstance(enhanced_image, str):
        enhanced = Image.open(enhanced_image).convert('RGB')
    else:
        enhanced = enhanced_image
    
    # Convert to numpy arrays
    orig_array = np.array(original)
    enh_array = np.array(enhanced)
    
    # Create figure
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Image Enhancement Analysis', fontsize=16)
    
    # Plot original and enhanced images
    axs[0, 0].imshow(orig_array)
    axs[0, 0].set_title('Original Image')
    axs[0, 0].axis('off')
    
    axs[0, 1].imshow(enh_array)
    axs[0, 1].set_title('Enhanced Image')
    axs[0, 1].axis('off')
    
    # Plot histograms
    orig_gray = np.array(original.convert('L'))
    enh_gray = np.array(enhanced.convert('L'))
    
    axs[0, 2].hist(orig_gray.flatten(), bins=256, alpha=0.7, color='blue', range=(0, 255))
    axs[0, 2].hist(enh_gray.flatten(), bins=256, alpha=0.7, color='red', range=(0, 255))
    axs[0, 2].set_title('Grayscale Histogram')
    axs[0, 2].legend(['Original', 'Enhanced'])
    axs[0, 2].set_xlim([0, 255])
    
    # Plot RGB channels histograms
    colors = ['red', 'green', 'blue']
    for i, color in enumerate(colors):
        # Original image
        axs[1, i].hist(orig_array[:,:,i].flatten(), bins=256, alpha=0.7, color=color, range=(0, 255))
        # Enhanced image
        axs[1, i].hist(enh_array[:,:,i].flatten(), bins=256, alpha=0.7, color='darkgray', range=(0, 255))
        axs[1, i].set_title(f'{color.capitalize()} Channel')
        axs[1, i].legend(['Original', 'Enhanced'])
        axs[1, i].set_xlim([0, 255])
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Add enhancement parameters text
    param_text = f"Applied: "
    changes = []
    
    if params.brightness != 1.0:
        changes.append(f"Brightness={params.brightness:.2f}")
    if params.contrast != 1.0:
        changes.append(f"Contrast={params.contrast:.2f}")
    if params.sharpness != 1.0:
        changes.append(f"Sharpness={params.sharpness:.2f}")
    if params.color != 1.0:
        changes.append(f"Color={params.color:.2f}")
    if params.denoise:
        changes.append("Denoise")
    if params.binarize:
        changes.append(f"Binarize(t={params.binarize_threshold})")
    if params.deskew:
        changes.append("Deskew")
    if params.resize_factor is not None:
        changes.append(f"Resize({params.resize_factor:.2f}x)")
        
    if changes:
        param_text += ", ".join(changes)
    else:
        param_text += "No changes"
        
    plt.figtext(0.5, 0.01, param_text, ha='center', fontsize=10, 
               bbox={"facecolor":"orange", "alpha":0.2, "pad":5})
    
    # Save plot if path provided
    if save_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
        plt.savefig(save_path, dpi=150)
    
    # Show plot if requested
    if show_plot:
        plt.show()
    else:
        plt.close(fig)
        
def get_supported_formats() -> List[str]:
    """
    Get list of supported image formats for input/output
    
    Returns:
        List of supported image format extensions
    """
    return ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'] 