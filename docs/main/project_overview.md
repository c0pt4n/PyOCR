# PyOCR Project Overview

## Project Description
PyOCR (Python Optical Character Recognition) is a desktop application that provides a graphical user interface for the Tesseract OCR engine. The application allows users to extract text from images using optical character recognition technology with an intuitive and user-friendly interface built with PyQt.

## Project Goals
1. Create a cross-platform GUI application for Tesseract OCR
2. Implement image preprocessing capabilities to improve OCR accuracy
3. Support multiple output formats
4. Provide a user-friendly interface for OCR operations
5. Ensure cross-platform compatibility (Windows, macOS, Linux)

## Key Features

### GUI Interface
- Modern PyQt-based user interface
- Responsive design that adapts to different screen sizes
- Threading implementation to prevent UI freezing during processing
- Progress indicators for OCR operations

### File Handling
- Support for multiple image formats (PNG, JPEG, TIFF)
- Automatic format conversion for unsupported formats
- File preview functionality
- File size limitations and validation
- Cross-platform file path handling

### Text Output Options
- Multiple output formats:
  - Plain text
  - hOCR (HTML)
  - PDF
  - Invisible-text-only PDF
  - TSV
  - ALTO
  - PAGE
- File saving with proper extension handling
- Clipboard functionality (copy/paste)
- Auto-copy option after OCR completion

### Image Processing
- Basic preprocessing pipeline using OpenCV:
  - Grayscale conversion
  - Noise reduction
  - Contrast enhancement
  - Thresholding
- Document-specific preprocessing:
  - Edge detection
  - Perspective correction
  - Border removal
  - Shadow elimination
- AI-enhanced image quality improvement using transfer learning models

## Technical Architecture

### Core Components
1. **Main Application**: Handles the application lifecycle and coordinates between components
2. **UI Layer**: PyQt-based user interface components
3. **OCR Engine**: Integration with Tesseract OCR via pytesseract
4. **Image Processing**: OpenCV-based preprocessing pipeline
5. **File I/O**: Handles file reading/writing operations

### Dependencies
- PyQt6: UI framework
- pytesseract: Python wrapper for Tesseract OCR
- OpenCV (cv2): Image processing library
- Pillow: Python Imaging Library
- NumPy: Numerical computing library
- Matplotlib: Visualization library (for debugging and development)

### Directory Structure
```
PyOCR/
├── docs/               # Documentation
│   ├── main/          # Project overview and main documentation
│   ├── img_enhance/   # Documentation for image enhancement module
│   ├── tests/         # Test documentation
│   └── pdfs/          # PDF documentation
├── src/               # Source code
│   ├── img_enhance/   # Image enhancement module
│   ├── main.py        # Main entry point
│   └── mainui.py      # Main UI implementation
├── tests/             # Test files
├── requirements.txt   # Project dependencies
└── README.md          # Project README
```

## Implementation Details

### OCR Integration
The application integrates with Tesseract OCR through the pytesseract library. The OCR process is executed in a separate thread to prevent UI freezing during processing, with progress updates shown to the user.

### Image Enhancement
The image enhancement module provides various preprocessing techniques to improve OCR accuracy:
1. **Basic Processing**: Grayscale conversion, noise reduction, contrast enhancement
2. **Advanced Processing**: Edge detection, perspective correction, shadow removal
3. **AI-Enhanced Processing**: Transfer learning models for image quality improvement

### Cross-Platform Compatibility
The application is designed to work across different operating systems:
- Windows file path handling
- macOS file path handling
- Linux file path handling

### User Interface
The UI is built with PyQt6 and includes:
- File selection dialog
- Image preview area
- Text output display
- Format selection options
- Processing options
- Progress indicators

## Development Roadmap

### Phase 1: Basic Functionality
- Project setup and environment configuration
- Basic PyQt window structure
- Tesseract integration
- Simple file selection and OCR processing

### Phase 2: Enhanced Features
- Image preprocessing pipeline
- Multiple output formats
- Clipboard functionality
- File saving options

### Phase 3: Advanced Features
- AI-enhanced image processing
- Batch processing capabilities
- Advanced document preprocessing
- User preference saving

### Phase 4: Optimization and Refinement
- Performance optimization
- UI/UX improvements
- Cross-platform testing and fixes
- Documentation completion

## Team Members
1. Omar Mohamed Mahmoud Ibrahim
2. Mohamed Ahmed Mohamed Ali Shehata
3. Mohamed Ahmed Mohamed Atta
4. Omar Mohamed Abdo
5. Salah Eldin Mohamed Salah
6. Hussein Arafat 