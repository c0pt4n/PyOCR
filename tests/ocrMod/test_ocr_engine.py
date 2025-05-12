"""
Tests for the OCR Engine module
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from PIL import Image

# Import the OCREngine class
from src.ocrMod.ocr_engine import OCREngine


class TestOCREngine(unittest.TestCase):
    """Test cases for OCREngine class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.ocr_engine = OCREngine()
        
        # Create a test directory path
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_resources_dir = os.path.join(self.test_dir, 'resources')
        
        # Ensure test resources directory exists
        os.makedirs(self.test_resources_dir, exist_ok=True)
    
    @patch('src.ocrMod.ocr_engine.pytesseract')
    @patch('src.ocrMod.ocr_engine.Image.open')
    @patch('src.ocrMod.ocr_engine.os.path.exists')
    def test_process_image_text_format(self, mock_exists, mock_image_open, mock_pytesseract):
        """Test processing an image with text output format"""
        # Mock file existence
        mock_exists.return_value = True
        
        # Mock image
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        
        # Mock pytesseract response
        expected_text = "Sample OCR Text"
        mock_pytesseract.image_to_string.return_value = expected_text
        
        # Test the method
        result = self.ocr_engine.process_image(
            image_path="dummy_path.jpg",
            lang="eng",
            output_format="text"
        )
        
        # Assertions
        self.assertEqual(result, expected_text)
        mock_pytesseract.image_to_string.assert_called_once_with(
            mock_img, lang="eng", config=""
        )
    
    @patch('src.ocrMod.ocr_engine.pytesseract')
    def test_process_pil_image(self, mock_pytesseract):
        """Test processing a PIL Image directly"""
        # Create a mock PIL Image
        mock_img = MagicMock(spec=Image.Image)
        
        # Mock pytesseract response
        expected_text = "Direct PIL Image OCR Text"
        mock_pytesseract.image_to_string.return_value = expected_text
        
        # Test the method
        result = self.ocr_engine.process_pil_image(
            image=mock_img,
            lang="eng",
            output_format="text"
        )
        
        # Assertions
        self.assertEqual(result, expected_text)
        mock_pytesseract.image_to_string.assert_called_once_with(
            mock_img, lang="eng", config=""
        )
    
    @patch('src.ocrMod.ocr_engine.pytesseract')
    @patch('src.ocrMod.ocr_engine.Image.open')
    @patch('src.ocrMod.ocr_engine.os.path.exists')
    def test_process_image_hocr_format(self, mock_exists, mock_image_open, mock_pytesseract):
        """Test processing an image with hOCR output format"""
        # Mock file existence
        mock_exists.return_value = True
        
        # Mock image
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        
        # Mock pytesseract response
        expected_hocr = "<div class='ocr_page'>Sample hOCR</div>"
        mock_pytesseract.image_to_pdf_or_hocr.return_value = expected_hocr
        
        # Test the method
        result = self.ocr_engine.process_image(
            image_path="dummy_path.jpg",
            lang="eng",
            output_format="hocr"
        )
        
        # Assertions
        self.assertEqual(result, expected_hocr)
        mock_pytesseract.image_to_pdf_or_hocr.assert_called_once_with(
            mock_img, lang="eng", extension='hocr', config=""
        )
    
    @patch('src.ocrMod.ocr_engine.os.path.exists')
    def test_process_image_file_not_found(self, mock_exists):
        """Test error handling when file doesn't exist"""
        # Mock file not existing
        mock_exists.return_value = False
        
        # Test the method raises FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            self.ocr_engine.process_image(
                image_path="nonexistent_file.jpg"
            )
    
    @patch('src.ocrMod.ocr_engine.pytesseract')
    @patch('src.ocrMod.ocr_engine.Image.open')
    @patch('src.ocrMod.ocr_engine.os.path.exists')
    def test_process_image_invalid_format(self, mock_exists, mock_image_open, mock_pytesseract):
        """Test error handling with invalid output format"""
        # Mock file existence
        mock_exists.return_value = True
        
        # Mock image
        mock_img = MagicMock()
        mock_image_open.return_value = mock_img
        
        # Test the method raises ValueError
        with self.assertRaises(ValueError):
            self.ocr_engine.process_image(
                image_path="dummy_path.jpg",
                output_format="invalid_format"
            )


if __name__ == '__main__':
    unittest.main() 