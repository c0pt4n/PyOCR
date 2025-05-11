import pytest
import os
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import shutil

@pytest.fixture
def test_image_path():
    """Create a temporary test image file and return its path"""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        # Create a simple test image
        img = Image.new('RGB', (300, 200), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Draw some text
        try:
            font = ImageFont.truetype("Arial", 20)
        except IOError:
            font = ImageFont.load_default()
            
        draw.text((50, 50), "Test Image", fill=(0, 0, 0), font=font)
        draw.text((50, 100), "For OCR Testing", fill=(0, 0, 0), font=font)
        
        # Draw some shapes
        draw.rectangle([200, 50, 250, 100], outline=(0, 0, 0))
        draw.line([50, 150, 250, 150], fill=(0, 0, 0), width=2)
        
        # Save the image
        img.save(tmp.name)
        
    yield tmp.name
    
    # Cleanup
    if os.path.exists(tmp.name):
        os.unlink(tmp.name)

@pytest.fixture
def noisy_image_path():
    """Create a temporary noisy test image file and return its path"""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        # Create a simple test image
        img = Image.new('RGB', (300, 200), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Draw some text
        try:
            font = ImageFont.truetype("Arial", 20)
        except IOError:
            font = ImageFont.load_default()
            
        draw.text((50, 50), "Noisy Image", fill=(0, 0, 0), font=font)
        draw.text((50, 100), "With Noise", fill=(0, 0, 0), font=font)
        
        # Save the image
        img.save(tmp.name)
        
        # Add noise using numpy
        img_array = np.array(img)
        noise = np.random.randint(0, 50, img_array.shape, dtype=np.uint8)
        noisy_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
        
        # Convert back to PIL image and save
        noisy_img = Image.fromarray(noisy_array)
        noisy_img.save(tmp.name)
        
    yield tmp.name
    
    # Cleanup
    if os.path.exists(tmp.name):
        os.unlink(tmp.name)

@pytest.fixture
def dark_image_path():
    """Create a temporary dark test image file and return its path"""
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        # Create a simple test image
        img = Image.new('RGB', (300, 200), color=(50, 50, 50))
        draw = ImageDraw.Draw(img)
        
        # Draw some text
        try:
            font = ImageFont.truetype("Arial", 20)
        except IOError:
            font = ImageFont.load_default()
            
        draw.text((50, 50), "Dark Image", fill=(150, 150, 150), font=font)
        draw.text((50, 100), "Low Light", fill=(150, 150, 150), font=font)
        
        # Save the image
        img.save(tmp.name)
        
    yield tmp.name
    
    # Cleanup
    if os.path.exists(tmp.name):
        os.unlink(tmp.name)

@pytest.fixture
def temp_output_dir():
    """Create a temporary directory for output files"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def load_test_images():
    """Load multiple test images into memory"""
    # Create test images
    images = {}
    
    # Standard test image
    img = Image.new('RGB', (300, 200), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("Arial", 20)
    except IOError:
        font = ImageFont.load_default()
    draw.text((50, 50), "Standard Test", fill=(0, 0, 0), font=font)
    images['standard'] = img.copy()
    
    # Blurry image
    blurry = img.copy()
    blurry = blurry.filter(ImageFilter.GaussianBlur(radius=2))
    images['blurry'] = blurry
    
    # Dark image
    dark = Image.new('RGB', (300, 200), color=(50, 50, 50))
    draw = ImageDraw.Draw(dark)
    draw.text((50, 50), "Dark Test", fill=(150, 150, 150), font=font)
    images['dark'] = dark
    
    # High contrast image
    contrast = Image.new('RGB', (300, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(contrast)
    draw.text((50, 50), "High Contrast", fill=(0, 0, 0), font=font)
    images['contrast'] = contrast
    
    return images 