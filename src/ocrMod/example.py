#!/usr/bin/env python3
"""
Example script demonstrating how to use the OCR module
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path to make imports work
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.ocrMod.ocr_engine import OCREngine


def main():
    """
    Main function demonstrating OCR module usage
    """
    # Check if an image path was provided
    if len(sys.argv) < 2:
        print("Usage: python example.py <image_path> [output_format] [language]")
        print("Available output formats: text, hocr, pdf, tsv, alto, page")
        print("Default output format: text")
        print("Default language: eng (English)")
        return 1
    
    # Get command line arguments
    image_path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "text"
    language = sys.argv[3] if len(sys.argv) > 3 else "eng"
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return 1
    
    try:
        # Initialize the OCR engine
        ocr = OCREngine()
        
        # Process the image
        print(f"Processing image: {image_path}")
        print(f"Language: {language}")
        print(f"Output format: {output_format}")
        
        result = ocr.process_image(
            image_path=image_path,
            lang=language,
            output_format=output_format
        )
        
        # Print or save the result based on output format
        if output_format == "text":
            print("\nExtracted Text:")
            print("-" * 40)
            print(result)
        elif output_format in ["pdf", "hocr", "alto"]:
            # For binary formats, save to a file
            output_file = f"output.{output_format}"
            with open(output_file, "wb") as f:
                f.write(result)
            print(f"\nOutput saved to: {output_file}")
        else:
            # For other formats like TSV, just print the first few lines
            print("\nExtracted Data (first few lines):")
            print("-" * 40)
            print(str(result)[:500] + "...")
            
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 