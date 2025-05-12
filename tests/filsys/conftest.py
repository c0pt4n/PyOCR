"""
Pytest configuration for file system handler tests.
"""
import sys
import os
import pytest
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import PyQt6 for QApplication
from PyQt6.QtWidgets import QApplication


# Create a QApplication instance for all tests
@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for the tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


# Create a fixture for temporary test files
@pytest.fixture
def temp_image_files(tmp_path):
    """Create temporary test image files with different extensions."""
    # Create test files with different extensions
    test_files = {}
    for ext in ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.txt']:
        file_path = tmp_path / f'test_file{ext}'
        with open(file_path, 'w') as f:
            f.write('test content')
        test_files[ext] = str(file_path)
    
    return tmp_path, test_files 