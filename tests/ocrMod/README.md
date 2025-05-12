# OCR Module Tests

This directory contains tests for the OCR (Optical Character Recognition) module.

## Test Files

- Tests for Tesseract integration
- Tests for text extraction functionality
- Tests for different output formats
- Tests for threading and performance

## Running the Tests

To run the tests, use the following command from the project root directory:

```bash
PYTHONPATH=$PWD pytest tests/ocrMod -v
```

## Test Coverage

The tests cover:

- Tesseract engine initialization and configuration
- Cross-platform compatibility
- Text extraction from various image types
- Output format handling (plain text, hOCR, PDF, TSV, ALTO, PAGE)
- Threading implementation for UI responsiveness
- Progress indication functionality
- Error handling and validation
- Clipboard operations

## Test Data

The tests use sample images located in the test data directory. These include:

- Text documents in various languages
- Images with different fonts and styles
- Scanned documents with various quality levels
- Images with mixed content (text and graphics)

## Mock Testing

Where appropriate, tests use mocking to:

- Simulate Tesseract engine responses
- Test error handling and edge cases
- Verify proper threading behavior
- Test UI interactions without actual rendering

## Adding New Tests

When adding new tests:

1. Follow the existing test structure and naming conventions
2. Add appropriate test images to the test data directory
3. Mock external dependencies like Tesseract when appropriate
4. Test both success and failure scenarios
5. Verify output formats match expected structures 