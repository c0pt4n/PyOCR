import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import QApplication, QMainWindow

from src.filsys.demo import FileSystemDemo


# Create a QApplication instance for the tests
@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for the tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


class TestFileSystemDemo:
    """Tests for the FileSystemDemo class."""
    
    @pytest.fixture
    def demo(self, qapp):
        """Create a FileSystemDemo instance."""
        return FileSystemDemo()
    
    def test_init(self, demo):
        """Test initialization of FileSystemDemo."""
        assert isinstance(demo, QMainWindow)
        assert demo.windowTitle() == "File System Handler Demo"
        assert demo.minimumSize().width() >= 600
        assert demo.minimumSize().height() >= 400
        assert demo.file_handler is not None
        assert demo.selected_file is None
    
    def test_setup_ui(self, demo):
        """Test that the UI is set up correctly."""
        # Check that the title label exists
        central_widget = demo.centralWidget()
        layout = central_widget.layout()
        
        # Check that the results text area exists
        assert hasattr(demo, 'results_text')
        assert demo.results_text.isReadOnly()
    
    def test_log_result(self, demo):
        """Test the log_result method."""
        # Initial state
        initial_text = demo.results_text.toPlainText()
        
        # Log a message
        demo._log_result("Test message")
        
        # Check that the message was added
        new_text = demo.results_text.toPlainText()
        assert new_text != initial_text
        assert "Test message" in new_text
    
    @patch('src.filsys.file_handler.FileSystemHandler.select_image_file')
    def test_on_select_file_clicked(self, mock_select, demo):
        """Test the select file button click handler."""
        # Mock the select_image_file method to return a file path
        mock_select.return_value = '/path/to/selected/image.png'
        
        # Also mock validate_file_type to return True
        demo.file_handler.validate_file_type = MagicMock(return_value=True)
        
        # Call the method
        demo._on_select_file_clicked()
        
        # Check that select_image_file was called
        mock_select.assert_called_once()
        
        # Check that the selected file was set
        assert demo.selected_file == '/path/to/selected/image.png'
        
        # Check that validate_file_type was called
        demo.file_handler.validate_file_type.assert_called_once_with('/path/to/selected/image.png')
        
        # Check that the results were logged
        result_text = demo.results_text.toPlainText()
        assert "Selected file: /path/to/selected/image.png" in result_text
        assert "File type is valid" in result_text
    
    @patch('src.filsys.file_handler.FileSystemHandler.select_image_file')
    def test_on_select_file_clicked_invalid_type(self, mock_select, demo):
        """Test the select file button click handler with an invalid file type."""
        # Mock the select_image_file method to return a file path
        mock_select.return_value = '/path/to/selected/invalid.txt'
        
        # Also mock validate_file_type to return False
        demo.file_handler.validate_file_type = MagicMock(return_value=False)
        
        # Call the method
        demo._on_select_file_clicked()
        
        # Check that the selected file was set
        assert demo.selected_file == '/path/to/selected/invalid.txt'
        
        # Check that validate_file_type was called
        demo.file_handler.validate_file_type.assert_called_once_with('/path/to/selected/invalid.txt')
        
        # Check that the results were logged
        result_text = demo.results_text.toPlainText()
        assert "Selected file: /path/to/selected/invalid.txt" in result_text
        assert "File type is not supported" in result_text
    
    @patch('src.filsys.file_handler.FileSelectionDialog.get_image_file')
    def test_on_select_file_enhanced_clicked(self, mock_get_file, demo):
        """Test the enhanced select file button click handler."""
        # Mock the get_image_file method to return a file path
        mock_get_file.return_value = '/path/to/selected/image.png'
        
        # Call the method
        demo._on_select_file_enhanced_clicked()
        
        # Check that get_image_file was called
        mock_get_file.assert_called_once_with(demo, demo.file_handler)
        
        # Check that the selected file was set
        assert demo.selected_file == '/path/to/selected/image.png'
        
        # Check that the results were logged
        result_text = demo.results_text.toPlainText()
        assert "Selected file (enhanced): /path/to/selected/image.png" in result_text
    
    @patch('src.filsys.file_handler.FileSystemHandler.select_directory')
    def test_on_select_dir_clicked(self, mock_select_dir, demo):
        """Test the select directory button click handler."""
        # Mock the select_directory method to return a directory path
        mock_select_dir.return_value = '/path/to/selected/directory'
        
        # Call the method
        demo._on_select_dir_clicked()
        
        # Check that select_directory was called
        mock_select_dir.assert_called_once()
        
        # Check that the results were logged
        result_text = demo.results_text.toPlainText()
        assert "Selected directory: /path/to/selected/directory" in result_text
    
    @patch('src.filsys.file_handler.FileSystemHandler.select_output_file')
    def test_on_save_file_clicked(self, mock_select_output, demo):
        """Test the save file button click handler."""
        # Mock the select_output_file method to return a file path and format
        mock_select_output.return_value = ('/path/to/output/file.txt', 'txt')
        
        # Call the method
        demo._on_save_file_clicked()
        
        # Check that select_output_file was called
        mock_select_output.assert_called_once()
        
        # Check that the results were logged
        result_text = demo.results_text.toPlainText()
        assert "Save location: /path/to/output/file.txt" in result_text
        assert "Format: txt" in result_text
    
    @patch('src.filsys.file_handler.SaveFileDialog.get_save_location')
    def test_on_save_file_enhanced_clicked(self, mock_get_location, demo):
        """Test the enhanced save file button click handler."""
        # Mock the get_save_location method to return a file path, format, and auto-copy flag
        mock_get_location.return_value = ('/path/to/output/file.txt', 'txt', True)
        
        # Call the method
        demo._on_save_file_enhanced_clicked()
        
        # Check that get_save_location was called
        mock_get_location.assert_called_once_with(demo, demo.file_handler)
        
        # Check that the results were logged
        result_text = demo.results_text.toPlainText()
        assert "Save location (enhanced): /path/to/output/file.txt" in result_text
        assert "Format: txt" in result_text
        assert "Auto-copy: True" in result_text 