import pytest
import os
import json
import tempfile
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

from src.img_enhance.utils import (
    save_params_to_json,
    load_params_from_json,
    create_comparison_image,
    plot_enhancement_metrics,
    get_supported_formats
)
from src.img_enhance.enhancer import EnhancementParams

class TestParamsJsonUtils:
    """Tests for parameter JSON saving/loading functions"""
    
    def test_save_params_to_json(self, temp_output_dir):
        """Test saving parameters to JSON file"""
        # Create test parameters
        params = EnhancementParams(
            brightness=1.2,
            contrast=1.5,
            sharpness=1.8,
            color=0.9,
            denoise=True
        )
        
        # Save to file
        output_path = os.path.join(temp_output_dir, "params.json")
        save_params_to_json(params, output_path)
        
        # Check that file exists
        assert os.path.exists(output_path)
        
        # Check file contents
        with open(output_path, 'r') as f:
            data = json.load(f)
            
        assert data['brightness'] == 1.2
        assert data['contrast'] == 1.5
        assert data['sharpness'] == 1.8
        assert data['color'] == 0.9
        assert data['denoise'] is True
    
    def test_load_params_from_json(self, temp_output_dir):
        """Test loading parameters from JSON file"""
        # Create JSON file
        params_data = {
            'brightness': 1.3,
            'contrast': 1.6,
            'sharpness': 1.9,
            'denoise': True,
            'binarize': True
        }
        
        json_path = os.path.join(temp_output_dir, "test_params.json")
        with open(json_path, 'w') as f:
            json.dump(params_data, f)
        
        # Load parameters
        params = load_params_from_json(json_path)
        
        # Check values
        assert params.brightness == 1.3
        assert params.contrast == 1.6
        assert params.sharpness == 1.9
        assert params.denoise is True
        assert params.binarize is True
        assert params.color == 1.0  # Default value
    
    def test_save_load_cycle(self, temp_output_dir):
        """Test saving and then loading parameters"""
        # Original parameters
        original_params = EnhancementParams(
            brightness=1.4,
            contrast=1.7,
            binarize=True,
            binarize_threshold=150
        )
        
        # Save to file
        output_path = os.path.join(temp_output_dir, "cycle_params.json")
        save_params_to_json(original_params, output_path)
        
        # Load back
        loaded_params = load_params_from_json(output_path)
        
        # Check that values match
        assert loaded_params.brightness == original_params.brightness
        assert loaded_params.contrast == original_params.contrast
        assert loaded_params.binarize == original_params.binarize
        assert loaded_params.binarize_threshold == original_params.binarize_threshold


class TestComparisonImage:
    """Tests for comparison image generation"""
    
    def test_create_comparison_image(self, load_test_images):
        """Test creating comparison image"""
        original = load_test_images['standard']
        enhanced = load_test_images['contrast']  # Use contrast as "enhanced" version
        
        comparison = create_comparison_image(original, enhanced)
        
        # Result should be a valid image
        assert isinstance(comparison, Image.Image)
        
        # Output should be larger than inputs (to accommodate both images side by side)
        assert comparison.width > original.width
        assert comparison.height >= original.height  # Height might be the same
    
    def test_comparison_with_params(self, load_test_images, temp_output_dir):
        """Test comparison with parameter display"""
        original = load_test_images['standard']
        enhanced = load_test_images['contrast']
        
        params = EnhancementParams(
            brightness=1.2,
            contrast=1.5,
            denoise=True
        )
        
        comparison = create_comparison_image(original, enhanced, params)
        
        # Result should be a valid image
        assert isinstance(comparison, Image.Image)
        
        # Height should be even larger to accommodate parameter text
        assert comparison.height > original.height
        
        # Save image to verify it works
        output_path = os.path.join(temp_output_dir, "comparison.png")
        comparison.save(output_path)
        assert os.path.exists(output_path)
    
    def test_comparison_different_sizes(self, load_test_images):
        """Test comparison with different size images"""
        original = load_test_images['standard']
        
        # Create a different size image
        smaller = original.resize((original.width // 2, original.height // 2))
        
        comparison = create_comparison_image(original, smaller)
        
        # Should still work and create a valid image
        assert isinstance(comparison, Image.Image)


class TestMetricsPlotting:
    """Tests for metrics plotting function"""
    
    def test_plot_enhancement_metrics(self, load_test_images, temp_output_dir, monkeypatch):
        """Test metrics plotting"""
        # Mock plt.show to avoid opening windows during tests
        monkeypatch.setattr(plt, 'show', lambda: None)
        
        original = load_test_images['standard']
        enhanced = load_test_images['contrast']
        params = EnhancementParams(brightness=1.2, contrast=1.5)
        
        # Test with show_plot=False
        plot_enhancement_metrics(
            original, enhanced, params, 
            show_plot=False,
        )
        
        # Test saving plot
        output_path = os.path.join(temp_output_dir, "metrics.png")
        plot_enhancement_metrics(
            original, enhanced, params, 
            show_plot=False,
            save_path=output_path
        )
        
        # File should exist
        assert os.path.exists(output_path)


class TestSupportedFormats:
    """Tests for supported format functions"""
    
    def test_get_supported_formats(self):
        """Test getting supported formats"""
        formats = get_supported_formats()
        
        # Should return a list of strings
        assert isinstance(formats, list)
        assert all(isinstance(fmt, str) for fmt in formats)
        
        # Should include common formats
        assert '.jpg' in formats
        assert '.png' in formats
        
        # All should start with a dot
        assert all(fmt.startswith('.') for fmt in formats) 