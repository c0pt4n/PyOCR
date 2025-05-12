# File System Handler Tests

This directory contains tests for the cross-platform file system handler module.

## Test Files

- `test_file_handler.py`: Tests for the `FileSystemHandler` class
- `test_dialogs.py`: Tests for the `FileSelectionDialog` and `SaveFileDialog` classes
- `test_demo.py`: Tests for the demo application

## Running the Tests

To run the tests, use the following command from the project root directory:

```bash
PYTHONPATH=$PWD pytest tests/filsys -v
```

## Test Coverage

The tests cover:

- File system handler initialization and configuration
- File type validation
- Recent files management
- File selection dialogs
- Save file dialogs
- Directory selection
- File path handling
- Demo application functionality

## Mock Testing

Many of the tests use mocking to avoid actual file system operations and UI interactions:

- `unittest.mock` is used to mock file dialogs and file system operations
- `QSignalSpy` is used to test Qt signal emissions
- Temporary files and directories are created for testing file operations

## Adding New Tests

When adding new tests:

1. Follow the existing test structure and naming conventions
2. Use appropriate fixtures for test setup
3. Mock external dependencies to keep tests fast and reliable
4. Test both success and error cases 