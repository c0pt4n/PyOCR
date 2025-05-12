import os
import sys
import tempfile
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.filsys.file_handler import FileSystemHandler


class TestFileSystemHandler:
    """Tests for the FileSystemHandler class."""
    
    @pytest.fixture
    def handler(self):
        """Create a FileSystemHandler instance with a mock parent."""
        parent_mock = MagicMock()
        return FileSystemHandler(parent_mock)
    
    @pytest.fixture
    def temp_files(self):
        """Create temporary test files with different extensions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files with different extensions
            test_files = {}
            for ext in ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.txt']:
                file_path = os.path.join(temp_dir, f'test_file{ext}')
                with open(file_path, 'w') as f:
                    f.write('test content')
                test_files[ext] = file_path
            
            yield temp_dir, test_files
    
    def test_init(self, handler):
        """Test initialization of FileSystemHandler."""
        assert handler.parent is not None
        assert isinstance(handler.recent_files, list)
        assert len(handler.recent_files) == 0
        assert handler.max_recent_files == 10
        assert handler.last_directory == str(Path.home())
    
    def test_validate_file_type_valid_extensions(self, handler, temp_files):
        """Test file type validation with valid extensions."""
        _, test_files = temp_files
        
        # Test valid image extensions
        assert handler.validate_file_type(test_files['.png']) is True
        assert handler.validate_file_type(test_files['.jpg']) is True
        assert handler.validate_file_type(test_files['.jpeg']) is True
        assert handler.validate_file_type(test_files['.tif']) is True
        assert handler.validate_file_type(test_files['.tiff']) is True
    
    def test_validate_file_type_invalid_extensions(self, handler, temp_files):
        """Test file type validation with invalid extensions."""
        _, test_files = temp_files
        
        # Test invalid image extension
        assert handler.validate_file_type(test_files['.txt']) is False
    
    def test_validate_file_type_nonexistent_file(self, handler):
        """Test file type validation with nonexistent file."""
        assert handler.validate_file_type('/path/to/nonexistent/file.png') is False
        assert handler.validate_file_type('') is False
        assert handler.validate_file_type(None) is False
    
    def test_add_to_recent_files(self, handler):
        """Test adding files to recent files list."""
        # Add a file
        handler._add_to_recent_files('/path/to/file1.png')
        assert len(handler.recent_files) == 1
        assert handler.recent_files[0] == '/path/to/file1.png'
        
        # Add another file
        handler._add_to_recent_files('/path/to/file2.png')
        assert len(handler.recent_files) == 2
        assert handler.recent_files[0] == '/path/to/file2.png'
        assert handler.recent_files[1] == '/path/to/file1.png'
        
        # Add existing file (should move to front)
        handler._add_to_recent_files('/path/to/file1.png')
        assert len(handler.recent_files) == 2
        assert handler.recent_files[0] == '/path/to/file1.png'
        assert handler.recent_files[1] == '/path/to/file2.png'
    
    def test_add_to_recent_files_limit(self, handler):
        """Test that recent files list is limited to max_recent_files."""
        # Set a smaller limit for testing
        handler.max_recent_files = 3
        
        # Add more files than the limit
        for i in range(5):
            handler._add_to_recent_files(f'/path/to/file{i}.png')
        
        # Check that only the most recent files are kept
        assert len(handler.recent_files) == 3
        assert handler.recent_files[0] == '/path/to/file4.png'
        assert handler.recent_files[1] == '/path/to/file3.png'
        assert handler.recent_files[2] == '/path/to/file2.png'
    
    def test_get_recent_files(self, handler):
        """Test getting the list of recent files."""
        # Add some files
        handler._add_to_recent_files('/path/to/file1.png')
        handler._add_to_recent_files('/path/to/file2.png')
        
        # Get recent files
        recent_files = handler.get_recent_files()
        assert len(recent_files) == 2
        assert recent_files[0] == '/path/to/file2.png'
        assert recent_files[1] == '/path/to/file1.png'
    
    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName')
    def test_select_image_file(self, mock_dialog, handler):
        """Test selecting an image file."""
        # Mock the file dialog to return a file path
        mock_dialog.return_value = ('/path/to/selected/image.png', 'PNG Files (*.png)')
        
        # Call the method
        result = handler.select_image_file()
        
        # Check that the dialog was called
        mock_dialog.assert_called_once()
        
        # Check that the result is correct
        assert result == '/path/to/selected/image.png'
        
        # Check that the last directory was updated
        assert handler.last_directory == '/path/to/selected'
        
        # Check that the file was added to recent files
        assert '/path/to/selected/image.png' in handler.recent_files
    
    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName')
    def test_select_image_file_canceled(self, mock_dialog, handler):
        """Test canceling the image file selection."""
        # Mock the file dialog to return an empty path (canceled)
        mock_dialog.return_value = ('', '')
        
        # Call the method
        result = handler.select_image_file()
        
        # Check that the result is None
        assert result is None
        
        # Check that the last directory was not updated
        assert handler.last_directory == str(Path.home())
        
        # Check that no file was added to recent files
        assert len(handler.recent_files) == 0
    
    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName')
    def test_select_output_file(self, mock_dialog, handler):
        """Test selecting an output file."""
        # Mock the file dialog to return a file path
        mock_dialog.return_value = ('/path/to/output/file.txt', 'Plain Text (*.txt)')
        
        # Call the method
        result = handler.select_output_file()
        
        # Check that the dialog was called
        mock_dialog.assert_called_once()
        
        # Check that the result is correct
        assert result == ('/path/to/output/file.txt', 'txt')
        
        # Check that the last directory was updated
        assert handler.last_directory == '/path/to/output'
    
    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName')
    def test_select_output_file_with_default_format(self, mock_dialog, handler):
        """Test selecting an output file with a specific default format."""
        # Mock the file dialog to return a file path
        mock_dialog.return_value = ('/path/to/output/file.pdf', 'PDF (*.pdf)')
        
        # Call the method with a specific format
        result = handler.select_output_file(default_format='PDF')
        
        # Check that the dialog was called
        mock_dialog.assert_called_once()
        
        # Check that the result is correct
        assert result == ('/path/to/output/file.pdf', 'pdf')
    
    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName')
    def test_select_output_file_add_extension(self, mock_dialog, handler):
        """Test that the correct extension is added to the output file path."""
        # Mock the file dialog to return a file path without extension
        mock_dialog.return_value = ('/path/to/output/file', 'Plain Text (*.txt)')
        
        # Call the method
        result = handler.select_output_file()
        
        # Check that the extension was added
        assert result == ('/path/to/output/file.txt', 'txt')
    
    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName')
    def test_select_output_file_canceled(self, mock_dialog, handler):
        """Test canceling the output file selection."""
        # Mock the file dialog to return an empty path (canceled)
        mock_dialog.return_value = ('', '')
        
        # Call the method
        result = handler.select_output_file()
        
        # Check that the result is None
        assert result is None
        
        # Check that the last directory was not updated
        assert handler.last_directory == str(Path.home())
    
    @patch('PyQt6.QtWidgets.QFileDialog.getExistingDirectory')
    def test_select_directory(self, mock_dialog, handler):
        """Test selecting a directory."""
        # Mock the file dialog to return a directory path
        mock_dialog.return_value = '/path/to/selected/directory'
        
        # Call the method
        result = handler.select_directory()
        
        # Check that the dialog was called
        mock_dialog.assert_called_once()
        
        # Check that the result is correct
        assert result == '/path/to/selected/directory'
        
        # Check that the last directory was updated
        assert handler.last_directory == '/path/to/selected/directory'
    
    @patch('PyQt6.QtWidgets.QFileDialog.getExistingDirectory')
    def test_select_directory_canceled(self, mock_dialog, handler):
        """Test canceling the directory selection."""
        # Mock the file dialog to return an empty path (canceled)
        mock_dialog.return_value = ''
        
        # Call the method
        result = handler.select_directory()
        
        # Check that the result is None
        assert result is None
        
        # Check that the last directory was not updated
        assert handler.last_directory == str(Path.home()) 