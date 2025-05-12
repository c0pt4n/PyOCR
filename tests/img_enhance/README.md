# Image Enhancement Tests

This directory contains tests for the image enhancement module.

## Test Files

- Tests for image preprocessing functions
- Tests for document-specific enhancements
- Tests for optimization and caching mechanisms

## Running the Tests

To run the tests, use the following command from the project root directory:

```bash
PYTHONPATH=$PWD pytest tests/img_enhance -v
```

## Test Coverage

The tests cover:

- Grayscale conversion
- Noise reduction
- Contrast enhancement
- Thresholding
- Edge detection
- Perspective correction
- Border removal
- Shadow elimination
- Caching mechanisms
- Batch processing capabilities

## Test Data

The tests use sample images located in the test data directory. These include:

- Document scans
- Photos with text
- Images with various lighting conditions
- Images with perspective distortion

## Mock Testing

Where appropriate, tests use mocking to:

- Simulate image processing operations
- Test error handling
- Verify proper function calls
- Test performance optimizations

## Adding New Tests

When adding new tests:

1. Follow the existing test structure and naming conventions
2. Add appropriate test images to the test data directory
3. Test both normal operation and edge cases
4. Verify visual results where necessary using assertion helpers 