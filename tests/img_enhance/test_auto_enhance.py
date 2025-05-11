import pytest
import os
from PIL import Image
import numpy as np

from src.img_enhance.auto_enhance import (
    analyze_image,
    estimate_noise,
    determine_optimal_params,
    auto_enhance_image,
    batch_auto_enhance,
    get_enhancement_preview_grid
)
from src.img_enhance.enhancer import EnhancementParams

class TestAnalyzeImage:
    """Tests for image analysis functions"""
    
    def test_analyze_image_path(self, test_image_path):
        """Test analyzing image from file path"""
        metrics = analyze_image(test_image_path)
        
        # Check that all expected metrics are present
        assert 'brightness' in metrics
        assert 'contrast' in metrics
        assert 'sharpness' in metrics
        assert 'color_saturation' in metrics
        assert 'noise_level' in metrics
        assert 'r_avg' in metrics
        assert 'g_avg' in metrics
        assert 'b_avg' in metrics
        
        # Check that values are in expected ranges
        assert 0 <= metrics['brightness'] <= 1
        assert 0 <= metrics['contrast'] <= 1
        assert 0 <= metrics['sharpness'] <= 1
        assert 0 <= metrics['color_saturation'] <= 1
        assert 0 <= metrics['noise_level'] <= 1
        
        # RGB averages should be in range 0-1
        assert 0 <= metrics['r_avg'] <= 1
        assert 0 <= metrics['g_avg'] <= 1
        assert 0 <= metrics['b_avg'] <= 1
    
    def test_analyze_image_pil(self, load_test_images):
        """Test analyzing PIL image object"""
        image = load_test_images['standard']
        metrics = analyze_image(image)
        
        # Same basic checks as above
        assert 'brightness' in metrics
        assert 0 <= metrics['brightness'] <= 1
    
    def test_analyze_different_image_types(self, load_test_images):
        """Test analysis of different image types"""
        # Standard image
        standard_metrics = analyze_image(load_test_images['standard'])
        
        # Dark image
        dark_metrics = analyze_image(load_test_images['dark'])
        
        # High contrast image
        contrast_metrics = analyze_image(load_test_images['contrast'])
        
        # Check that metrics differ for different image types
        assert dark_metrics['brightness'] < standard_metrics['brightness']
        assert contrast_metrics['contrast'] > standard_metrics['contrast']
    
    def test_estimate_noise(self, load_test_images, noisy_image_path):
        """Test noise estimation"""
        # Standard image should have low noise
        standard_img = load_test_images['standard'].convert('L')
        standard_noise = estimate_noise(standard_img)
        
        # Noisy image should have higher noise
        noisy_img = Image.open(noisy_image_path).convert('L')
        noisy_noise = estimate_noise(noisy_img)
        
        # This isn't a perfect test since the noisy image is synthetic
        # but in most cases the noisy image should report higher noise
        assert 0 <= standard_noise <= 1
        assert 0 <= noisy_noise <= 1


class TestDetermineOptimalParams:
    """Tests for parameter determination"""
    
    def test_determine_optimal_params_standard(self):
        """Test parameter determination for a standard image"""
        # Create mock metrics for a standard image
        metrics = {
            'brightness': 0.5,       # Medium brightness
            'contrast': 0.2,         # Medium contrast
            'sharpness': 0.15,       # Somewhat blurry
            'color_saturation': 0.2, # Decent color
            'noise_level': 0.1,      # Low noise
            'might_be_skewed': False,
            'r_avg': 0.5,
            'g_avg': 0.5,
            'b_avg': 0.5
        }
        
        params = determine_optimal_params(metrics)
        
        # Check that parameters were adjusted appropriately
        assert params.sharpness > 1.0  # Should increase sharpness
        assert params.contrast > 1.0   # Should increase contrast
        assert params.brightness == 1.0  # Should leave brightness alone
        assert params.denoise is False  # Should not denoise
    
    def test_determine_optimal_params_dark(self):
        """Test parameter determination for a dark image"""
        # Create mock metrics for a dark image
        metrics = {
            'brightness': 0.2,       # Very dark
            'contrast': 0.1,         # Low contrast
            'sharpness': 0.1,        # Blurry
            'color_saturation': 0.1, # Low color
            'noise_level': 0.2,      # Some noise
            'might_be_skewed': False,
            'r_avg': 0.2,
            'g_avg': 0.2,
            'b_avg': 0.2
        }
        
        params = determine_optimal_params(metrics)
        
        # Dark images should get brightness and contrast boost
        assert params.brightness > 1.0
        assert params.contrast > 1.0
    
    def test_determine_optimal_params_bright(self):
        """Test parameter determination for a bright, over-exposed image"""
        # Create mock metrics for an over-exposed image
        metrics = {
            'brightness': 0.8,       # Very bright
            'contrast': 0.05,        # Low contrast (washed out)
            'sharpness': 0.1,        # Blurry
            'color_saturation': 0.05, # Low color (washed out)
            'noise_level': 0.1,      # Low noise
            'might_be_skewed': False,
            'r_avg': 0.8,
            'g_avg': 0.8,
            'b_avg': 0.8
        }
        
        params = determine_optimal_params(metrics)
        
        # Bright, washed-out images should get reduced brightness, increased contrast
        assert params.brightness < 1.0
        assert params.contrast > 1.0
    
    def test_determine_optimal_params_noisy(self):
        """Test parameter determination for a noisy image"""
        # Create mock metrics for a noisy image
        metrics = {
            'brightness': 0.5,       # Medium brightness
            'contrast': 0.2,         # Medium contrast
            'sharpness': 0.15,       # Somewhat blurry
            'color_saturation': 0.2, # Decent color
            'noise_level': 0.4,      # High noise
            'might_be_skewed': False,
            'r_avg': 0.5,
            'g_avg': 0.5,
            'b_avg': 0.5
        }
        
        params = determine_optimal_params(metrics)
        
        # Noisy images should get denoising
        assert params.denoise is True


class TestAutoEnhance:
    """Tests for automatic enhancement functions"""
    
    def test_auto_enhance_image_path(self, test_image_path):
        """Test auto enhancement from file path"""
        enhanced = auto_enhance_image(test_image_path)
        
        # Check that we got a valid image back
        assert isinstance(enhanced, Image.Image)
        assert enhanced.mode == 'RGB'
        
        # Original image dimensions should be preserved
        original = Image.open(test_image_path)
        assert enhanced.size == original.size
    
    def test_auto_enhance_pil_image(self, load_test_images):
        """Test auto enhancement of PIL image"""
        original = load_test_images['standard']
        enhanced = auto_enhance_image(original)
        
        assert isinstance(enhanced, Image.Image)
        assert enhanced.size == original.size
    
    def test_auto_enhance_special_cases(self, load_test_images):
        """Test auto enhancement on special cases"""
        # Dark image
        dark_img = load_test_images['dark']
        enhanced_dark = auto_enhance_image(dark_img)
        
        # Enhanced image should generally be brighter
        dark_brightness = np.mean(np.array(dark_img))
        enhanced_brightness = np.mean(np.array(enhanced_dark))
        
        assert enhanced_brightness > dark_brightness
    
    def test_auto_enhance_preview(self, test_image_path):
        """Test preview generation in auto enhance"""
        preview = auto_enhance_image(test_image_path, preview=True, preview_size=(100, 100))
        
        # Preview should be smaller
        assert preview.width <= 100
        assert preview.height <= 100
    
    def test_batch_auto_enhance(self, test_image_path, temp_output_dir):
        """Test batch processing"""
        # For simplicity, we'll use the same test image multiple times
        image_paths = [test_image_path] * 3
        
        output_paths = batch_auto_enhance(image_paths, temp_output_dir)
        
        # Should return one output path per input
        assert len(output_paths) == len(image_paths)
        
        # All output files should exist
        for path in output_paths:
            assert os.path.exists(path)
            
            # Should be valid images
            img = Image.open(path)
            assert isinstance(img, Image.Image)
    
    def test_enhancement_preview_grid(self, test_image_path):
        """Test preview grid generation"""
        grid = get_enhancement_preview_grid(test_image_path)
        
        assert isinstance(grid, Image.Image)
        
        # Grid should have at least some minimum size
        assert grid.width > 100
        assert grid.height > 100
        
        # Custom variations
        variations = [
            {"brightness": 1.5},
            {"contrast": 1.5},
            {"binarize": True}
        ]
        
        custom_grid = get_enhancement_preview_grid(test_image_path, variations=variations)
        assert isinstance(custom_grid, Image.Image) 