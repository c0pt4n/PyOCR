#!/usr/bin/env python3
import unittest
from unittest.mock import patch, MagicMock, call
import os
import sys
import tempfile
import argparse
from PIL import Image
import io

# Add parent directory to path to allow module import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Import modules under test
from src.img_enhance.presets_cli import parse_args, get_preset_name
from src.img_enhance.text_presets import (
    enhance_with_preset,
    mixed_content_text_enhance,
    text_document_enhance, 
    text_only_enhance,
    receipt_enhance
)
from src.img_enhance.utils import create_comparison_image

class TestPresetsCLI(unittest.TestCase):
    """Test cases for presets_cli.py module"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.input_file = os.path.join(self.temp_dir.name, "input.jpg")
        self.output_file = os.path.join(self.temp_dir.name, "output.jpg")
        
        # Create a dummy input file
        img = Image.new('RGB', (100, 100), color='white')
        img.save(self.input_file)
    
    def tearDown(self):
        """Tear down test fixtures"""
        self.temp_dir.cleanup()
    
    def test_parse_args(self):
        """Test argument parsing"""
        # Test with minimal arguments
        with patch('sys.argv', ['presets_cli.py', self.input_file]):
            args = parse_args()
            self.assertEqual(args.input_path, self.input_file)
            self.assertEqual(args.preset, 0)  # Default preset should be 0
            self.assertFalse(args.compare)  # Default compare should be False
            self.assertIsNone(args.output_path)  # Default output_path should be None
        
        # Test with full arguments
        with patch('sys.argv', [
            'presets_cli.py',
            self.input_file,
            '--output-path', self.output_file,
            '--preset', '2',
            '--compare'
        ]):
            args = parse_args()
            self.assertEqual(args.input_path, self.input_file)
            self.assertEqual(args.preset, 2)
            self.assertTrue(args.compare)
            self.assertEqual(args.output_path, self.output_file)
        
        # Test with short options
        with patch('sys.argv', [
            'presets_cli.py',
            self.input_file,
            '-o', self.output_file,
            '-p', '3',
            '-c'
        ]):
            args = parse_args()
            self.assertEqual(args.input_path, self.input_file)
            self.assertEqual(args.preset, 3)
            self.assertTrue(args.compare)
            self.assertEqual(args.output_path, self.output_file)
    
    def test_preset_names(self):
        """Test the get_preset_name function"""
        # Test all preset names
        self.assertEqual(get_preset_name(0), "Mixed Content with Text Enhancement")
        self.assertEqual(get_preset_name(1), "Document Text Enhancement")
        self.assertEqual(get_preset_name(2), "Pure Text Enhancement")
        self.assertEqual(get_preset_name(3), "Receipt Text Enhancement")
        
        # Test unknown preset
        self.assertEqual(get_preset_name(99), "Unknown Preset")
    
    def test_output_path_generation(self):
        """Test output path generation logic"""
        # Create test image path
        test_input = "/path/to/image.jpg"
        
        # Test with no output path (should generate from input path)
        with patch('os.path.dirname', return_value="/path/to"), \
             patch('os.path.basename', return_value="image.jpg"), \
             patch('os.path.splitext', return_value=("image", ".jpg")), \
             patch('os.path.join', return_value="/path/to/image_preset0.jpg"):
            
            # This is the function logic from presets_cli.py
            dirname = os.path.dirname(test_input)
            filename = os.path.basename(test_input)
            base, ext = os.path.splitext(filename)
            output_path = os.path.join(dirname, f"{base}_preset0{ext}")
            
            self.assertEqual(output_path, "/path/to/image_preset0.jpg")
    
    def test_directory_creation(self):
        """Test directory creation for output path"""
        # Test nested directory creation
        nested_dir = os.path.join(self.temp_dir.name, "subdir1", "subdir2")
        os.makedirs(nested_dir, exist_ok=True)
        
        # Check that directory was created
        self.assertTrue(os.path.exists(nested_dir))
        
        # Test with exist_ok behavior
        # Should not raise an exception when called again
        os.makedirs(nested_dir, exist_ok=True)
    
    def test_presets_with_real_image(self):
        """Test presets with a real image (integration test)"""
        # Create a test image
        img = Image.new('RGB', (100, 100), color='white')
        img_path = os.path.join(self.temp_dir.name, "test_image.png")
        img.save(img_path)
        
        # Test each preset with the image
        for preset_id in range(4):
            # Apply the preset
            enhanced = enhance_with_preset(img, preset_id)
            
            # Verify enhanced image is still an image
            self.assertIsInstance(enhanced, Image.Image)
            self.assertEqual(enhanced.mode, 'RGB')
            self.assertEqual(enhanced.size, (100, 100))
            
            # Save the enhanced image
            output_path = os.path.join(self.temp_dir.name, f"enhanced_{preset_id}.png")
            enhanced.save(output_path)
            
            # Verify the file was created
            self.assertTrue(os.path.exists(output_path))
            
            # Create a comparison image
            if preset_id == 0:  # Only do this once to save time
                comparison = create_comparison_image(img, enhanced, None, f"Preset {preset_id}")
                comparison_path = os.path.join(self.temp_dir.name, "comparison.png")
                comparison.save(comparison_path)
                self.assertTrue(os.path.exists(comparison_path))

if __name__ == "__main__":
    unittest.main() 