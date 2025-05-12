# Cross-Platform File System Handler

This module provides a cross-platform file system handler for the PyOCR application, working seamlessly on Windows and Linux. It handles file selection and saving operations with support for various file formats.

## Features

- Cross-platform file path handling (Windows, Linux)
- File type validation for supported image formats (PNG, JPEG, TIFF)
- Enhanced file selection dialog with recent files list
- Enhanced save dialog with format selection
- Directory selection functionality
- Recent files tracking

## Usage

### Basic Usage

```python
from filsys.file_handler import FileSystemHandler

# Create a file system handler instance
file_handler = FileSystemHandler(parent_widget)

# Select an image file
file_path = file_handler.select_image_file()
if file_path:
    print(f"Selected file: {file_path}")

# Save output to a file
result = file_handler.select_output_file()
if result:
    file_path, format_name = result
    print(f"Save location: {file_path}")
    print(f"Format: {format_name}")

# Select a directory
directory = file_handler.select_directory()
if directory:
    print(f"Selected directory: {directory}")
```

### Enhanced Dialogs

```python
from filsys.file_handler import FileSelectionDialog, SaveFileDialog

# Enhanced file selection dialog
file_path = FileSelectionDialog.get_image_file(parent_widget)
if file_path:
    print(f"Selected file: {file_path}")

# Enhanced save dialog
result = SaveFileDialog.get_save_location(parent_widget)
if result:
    file_path, format_name, auto_copy = result
    print(f"Save location: {file_path}")
    print(f"Format: {format_name}")
    print(f"Auto-copy: {auto_copy}")
```

## Demo

Run the demo script to see the file system handler in action:

```bash
python src/filsys/demo.py
```

Or if you've made it executable:

```bash
./src/filsys/demo.py
``` 