import sys
import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import QApplication, QListWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from src.filsys.file_handler import FileSystemHandler, FileSelectionDialog, SaveFileDialog


# Create a QApplication instance for the tests
@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for the tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


class TestFileSelectionDialog:
    """Tests for the FileSelectionDialog class."""
    
    @pytest.fixture
    def file_handler(self):
        """Create a FileSystemHandler instance with mock recent files."""
        handler = FileSystemHandler()
        handler.recent_files = [
            '/path/to/recent1.png',
            '/path/to/recent2.jpg'
        ]
        return handler
    
    @pytest.fixture
    def dialog(self, qapp, file_handler):
        """Create a FileSelectionDialog instance."""
        return FileSelectionDialog(None, file_handler)
    
    def test_init(self, dialog, file_handler):
        """Test initialization of FileSelectionDialog."""
        assert dialog.file_handler == file_handler
        assert dialog.selected_file is None
        assert dialog.windowTitle() == "Select Image File"
        assert dialog.minimumSize().width() >= 600
        assert dialog.minimumSize().height() >= 400
    
    def test_setup_ui(self, dialog):
        """Test that the UI is set up correctly."""
        # Check that the type combo box is populated
        assert dialog.type_combo.count() > 0
        assert dialog.type_combo.itemText(0) == "All supported formats"
        
        # Check that the recent files list is populated
        assert hasattr(dialog, 'recent_list')
        assert dialog.recent_list.count() == 2
        
        # Check that the first item in the list is the most recent file
        first_item = dialog.recent_list.item(0)
        assert first_item.text() == "recent1.png"
        assert first_item.data(Qt.ItemDataRole.UserRole) == '/path/to/recent1.png'
    
    @patch('src.filsys.file_handler.FileSystemHandler.select_image_file')
    def test_on_browse_clicked(self, mock_select, dialog):
        """Test the browse button click handler."""
        # Mock the select_image_file method to return a file path
        mock_select.return_value = '/path/to/selected/image.png'
        
        # Create a spy for the file_selected signal
        signal_spy = QSignalSpy(dialog.file_selected)
        
        # Call the method
        dialog._on_browse_clicked()
        
        # Check that select_image_file was called
        mock_select.assert_called_once()
        
        # Check that the selected file was set
        assert dialog.selected_file == '/path/to/selected/image.png'
        
        # Check that the signal was emitted
        assert len(signal_spy) == 1
        assert signal_spy[0][0] == '/path/to/selected/image.png'
    
    @patch('src.filsys.file_handler.FileSystemHandler.select_image_file')
    def test_on_browse_clicked_canceled(self, mock_select, dialog):
        """Test the browse button click handler when selection is canceled."""
        # Mock the select_image_file method to return None (canceled)
        mock_select.return_value = None
        
        # Create a spy for the file_selected signal
        signal_spy = QSignalSpy(dialog.file_selected)
        
        # Call the method
        dialog._on_browse_clicked()
        
        # Check that select_image_file was called
        mock_select.assert_called_once()
        
        # Check that the selected file was not set
        assert dialog.selected_file is None
        
        # Check that the signal was not emitted
        assert len(signal_spy) == 0
    
    @patch('os.path.isfile')
    def test_on_recent_file_selected_exists(self, mock_isfile, dialog):
        """Test selecting a file from the recent files list that exists."""
        # Mock os.path.isfile to return True
        mock_isfile.return_value = True
        
        # Create a mock item
        item = MagicMock(spec=QListWidgetItem)
        item.data.return_value = '/path/to/recent1.png'
        
        # Create a spy for the file_selected signal
        signal_spy = QSignalSpy(dialog.file_selected)
        
        # Call the method
        dialog._on_recent_file_selected(item)
        
        # Check that the selected file was set
        assert dialog.selected_file == '/path/to/recent1.png'
        
        # Check that the signal was emitted
        assert len(signal_spy) == 1
        assert signal_spy[0][0] == '/path/to/recent1.png'
    
    @patch('os.path.isfile')
    @patch('PyQt6.QtWidgets.QMessageBox.warning')
    def test_on_recent_file_selected_not_exists(self, mock_warning, mock_isfile, dialog):
        """Test selecting a file from the recent files list that doesn't exist."""
        # Mock os.path.isfile to return False
        mock_isfile.return_value = False
        
        # Create a mock item
        item = MagicMock(spec=QListWidgetItem)
        item.data.return_value = '/path/to/nonexistent.png'
        
        # Mock the list widget's row method
        dialog.recent_list = MagicMock()
        dialog.recent_list.row.return_value = 0
        
        # Add the nonexistent file to the recent files
        dialog.file_handler.recent_files.append('/path/to/nonexistent.png')
        
        # Call the method
        dialog._on_recent_file_selected(item)
        
        # Check that a warning was shown
        mock_warning.assert_called_once()
        
        # Check that the file was removed from recent files
        assert '/path/to/nonexistent.png' not in dialog.file_handler.recent_files
        
        # Check that the item was removed from the list
        dialog.recent_list.takeItem.assert_called_once_with(0)


class TestSaveFileDialog:
    """Tests for the SaveFileDialog class."""
    
    @pytest.fixture
    def file_handler(self):
        """Create a FileSystemHandler instance."""
        return FileSystemHandler()
    
    @pytest.fixture
    def dialog(self, qapp, file_handler):
        """Create a SaveFileDialog instance."""
        return SaveFileDialog(None, file_handler)
    
    def test_init(self, dialog, file_handler):
        """Test initialization of SaveFileDialog."""
        assert dialog.file_handler == file_handler
        assert dialog.selected_file is None
        assert dialog.selected_format == "txt"
        assert dialog.windowTitle() == "Save Output"
        assert dialog.minimumSize().width() >= 500
        assert dialog.minimumSize().height() >= 300
    
    def test_setup_ui(self, dialog):
        """Test that the UI is set up correctly."""
        # Check that the format combo box is populated
        assert dialog.format_combo.count() > 0
        
        # Check that the auto-copy checkbox exists
        assert hasattr(dialog, 'auto_copy_cb')
        assert not dialog.auto_copy_cb.isChecked()
    
    @patch('src.filsys.file_handler.FileSystemHandler.select_output_file')
    def test_on_save_clicked(self, mock_select, dialog):
        """Test the save button click handler."""
        # Mock the select_output_file method to return a file path and format
        mock_select.return_value = ('/path/to/output/file.txt', 'txt')
        
        # Call the method
        dialog._on_save_clicked()
        
        # Check that select_output_file was called
        mock_select.assert_called_once()
        
        # Check that the selected file and format were set
        assert dialog.selected_file == '/path/to/output/file.txt'
        assert dialog.selected_format == 'txt'
    
    @patch('src.filsys.file_handler.FileSystemHandler.select_output_file')
    def test_on_save_clicked_canceled(self, mock_select, dialog):
        """Test the save button click handler when selection is canceled."""
        # Mock the select_output_file method to return None (canceled)
        mock_select.return_value = None
        
        # Call the method
        dialog._on_save_clicked()
        
        # Check that select_output_file was called
        mock_select.assert_called_once()
        
        # Check that the selected file was not set
        assert dialog.selected_file is None
        assert dialog.selected_format == "txt"  # Default value


# Helper class for testing signals
class QSignalSpy:
    """Simple implementation of a signal spy for testing Qt signals."""
    
    def __init__(self, signal):
        self.signal = signal
        self.args = []
        self.signal.connect(self.slot)
    
    def slot(self, *args):
        self.args.append(args)
    
    def __len__(self):
        return len(self.args)
    
    def __getitem__(self, index):
        return self.args[index] 