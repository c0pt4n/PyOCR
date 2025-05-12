"""
OCR Engine module that provides an interface to Tesseract OCR.
This module handles text extraction using the Tesseract engine.
"""

import os
import pytesseract
from PIL import Image
from typing import Optional, Union, Dict


class OCREngine:
    """
    OCR Engine class that provides methods to extract text from images using Tesseract.
    """
    
    def __init__(self, tesseract_cmd: Optional[str] = None):
        """
        Initialize the OCR engine.
        
        Args:
            tesseract_cmd: Path to the tesseract executable. If None, uses default.
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    
    def process_image(self, 
                      image_path: str, 
                      lang: str = 'eng',
                      output_format: str = 'text',
                      config: str = '') -> Union[str, Dict]:
        """
        Process an image and extract text using Tesseract OCR.
        
        Args:
            image_path: Path to the image file
            lang: Language(s) to use for OCR (default: 'eng')
            output_format: Output format ('text', 'hocr', 'pdf', 'tsv', 'alto', 'page')
            config: Additional configuration parameters for Tesseract
            
        Returns:
            Extracted text or data in the specified format
        """
        # Validate file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Open the image
        image = Image.open(image_path)
        
        # Process with tesseract based on requested output format
        result = self._extract_text(image, lang, output_format, config)
        
        return result
    
    def process_pil_image(self,
                         image: Image.Image,
                         lang: str = 'eng',
                         output_format: str = 'text',
                         config: str = '') -> Union[str, Dict]:
        """
        Process a PIL Image object directly and extract text using Tesseract OCR.
        
        Args:
            image: PIL Image object to process
            lang: Language(s) to use for OCR (default: 'eng')
            output_format: Output format ('text', 'hocr', 'pdf', 'tsv', 'alto', 'page')
            config: Additional configuration parameters for Tesseract
            
        Returns:
            Extracted text or data in the specified format
        """
        # Process with tesseract based on requested output format
        result = self._extract_text(image, lang, output_format, config)
        
        return result
    
    def _extract_text(self, 
                     image: Image.Image, 
                     lang: str, 
                     output_format: str, 
                     config: str) -> Union[str, Dict]:
        """
        Extract text from image using the appropriate tesseract method.
        
        Args:
            image: PIL Image object
            lang: Language(s) for OCR
            output_format: Output format
            config: Additional tesseract configuration
            
        Returns:
            Extracted text or data in the specified format
        """
        if output_format.lower() == 'text':
            return pytesseract.image_to_string(image, lang=lang, config=config)
        elif output_format.lower() == 'hocr':
            return pytesseract.image_to_pdf_or_hocr(image, lang=lang, extension='hocr', config=config)
        elif output_format.lower() == 'pdf':
            return pytesseract.image_to_pdf_or_hocr(image, lang=lang, extension='pdf', config=config)
        elif output_format.lower() == 'tsv':
            return pytesseract.image_to_data(image, lang=lang, config=config)
        elif output_format.lower() == 'alto':
            return pytesseract.image_to_alto_xml(image, lang=lang, config=config)
        elif output_format.lower() == 'page':
            # Note: Assuming pytesseract has this function (it might need custom implementation)
            # This is a placeholder for the PAGE format
            return pytesseract.image_to_string(image, lang=lang, config=f"{config} outputformat page")
        else:
            raise ValueError(f"Unsupported output format: {output_format}") 