#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import tempfile
from PIL import Image
import numpy as np

# Add parent directory to path to allow module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.img_enhance.text_presets import (
    mixed_content_text_enhance,
    text_document_enhance,
    text_only_enhance,
    receipt_enhance,
    get_preset_name,
    enhance_with_preset
)
from src.img_enhance.enhancer import EnhancementParams

class TestTextPresets(unittest.TestCase):
    """Test cases for text_presets.py module"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a simple test image (100x100 with some text-like features)
        self.test_img_size = (100, 100)
        self.test_img = Image.new('RGB', self.test_img_size, color='white')
        # Add some "text-like" black pixels
        pixels = self.test_img.load()
        for i in range(30, 70):
            for j in range(40, 60):
                if (i + j) % 3 == 0:  # Create a pattern
                    pixels[i, j] = (0, 0, 0)
        
        # Create a temporary file for saving tests
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file = os.path.join(self.temp_dir.name, "test_image.png")
        self.test_img.save(self.temp_file)
    
    def tearDown(self):
        """Tear down test fixtures"""
        self.temp_dir.cleanup()
    
    def test_mixed_content_text_enhance(self):
        """Test mixed_content_text_enhance function"""
        enhanced = mixed_content_text_enhance(self.test_img)
        
        # Check that output is an image
        self.assertIsInstance(enhanced, Image.Image)
        # Check that size is unchanged
        self.assertEqual(enhanced.size, self.test_img_size)
        # Check that some processing has occurred (image should not be identical)
        self.assertFalse(np.array_equal(np.array(enhanced), np.array(self.test_img)))
    
    def test_text_document_enhance(self):
        """Test text_document_enhance function"""
        enhanced = text_document_enhance(self.test_img)
        
        # Check that output is an image
        self.assertIsInstance(enhanced, Image.Image)
        # Check that size is unchanged
        self.assertEqual(enhanced.size, self.test_img_size)
        # Check that some processing has occurred
        self.assertFalse(np.array_equal(np.array(enhanced), np.array(self.test_img)))
    
    def test_text_only_enhance(self):
        """Test text_only_enhance function"""
        enhanced = text_only_enhance(self.test_img)
        
        # Check that output is an image
        self.assertIsInstance(enhanced, Image.Image)
        # Check that size is unchanged
        self.assertEqual(enhanced.size, self.test_img_size)
        # Check that some processing has occurred
        self.assertFalse(np.array_equal(np.array(enhanced), np.array(self.test_img)))
    
    def test_receipt_enhance(self):
        """Test receipt_enhance function"""
        enhanced = receipt_enhance(self.test_img)
        
        # Check that output is an image
        self.assertIsInstance(enhanced, Image.Image)
        # Check that size is unchanged
        self.assertEqual(enhanced.size, self.test_img_size)
        # Check that some processing has occurred
        self.assertFalse(np.array_equal(np.array(enhanced), np.array(self.test_img)))
        
        # Receipt should convert to grayscale (color=0.0)
        # Check if R, G, B values are equal for a sample of pixels
        enhanced_array = np.array(enhanced)
        sample_pixels = enhanced_array[40:50, 40:50]
        # In grayscale images, R=G=B for each pixel
        r_equals_g = np.all(sample_pixels[:,:,0] == sample_pixels[:,:,1])
        g_equals_b = np.all(sample_pixels[:,:,1] == sample_pixels[:,:,2])
        self.assertTrue(r_equals_g and g_equals_b, "Receipt enhance should convert to grayscale")
    
    def test_get_preset_name(self):
        """Test get_preset_name function"""
        self.assertEqual(get_preset_name(0), "Mixed Content with Text Enhancement")
        self.assertEqual(get_preset_name(1), "Document Text Enhancement")
        self.assertEqual(get_preset_name(2), "Pure Text Enhancement")
        self.assertEqual(get_preset_name(3), "Receipt Text Enhancement")
        self.assertEqual(get_preset_name(99), "Unknown Preset")  # Invalid ID
    
    def test_enhance_with_preset(self):
        """Test enhance_with_preset function"""
        # Test each preset ID
        for preset_id in range(4):
            enhanced = enhance_with_preset(self.test_img, preset_id)
            self.assertIsInstance(enhanced, Image.Image)
            self.assertEqual(enhanced.size, self.test_img_size)
        
        # Test with invalid preset ID (should default to mixed content)
        with patch('src.img_enhance.text_presets.mixed_content_text_enhance') as mock_enhance:
            mock_enhance.return_value = self.test_img  # Return original for simplicity
            enhance_with_preset(self.test_img, 99)
            mock_enhance.assert_called_once()
    
    def test_file_path_input(self):
        """Test functions with file path input instead of PIL Image"""
        # Test with file path
        enhanced = mixed_content_text_enhance(self.temp_file)
        self.assertIsInstance(enhanced, Image.Image)
        self.assertEqual(enhanced.size, self.test_img_size)
    
    def test_file_not_found(self):
        """Test error handling for non-existent files"""
        with self.assertRaises(FileNotFoundError):
            mixed_content_text_enhance("nonexistent_file.jpg")

if __name__ == "__main__":
    unittest.main() 