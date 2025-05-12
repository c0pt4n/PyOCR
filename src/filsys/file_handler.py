from pathlib import Path
import os
import platform
from typing import List, Tuple, Optional, Dict, Set

from PyQt6.QtWidgets import (
    QFileDialog, QWidget, QMessageBox, 
    QVBoxLayout, QPushButton, QLabel, 
    QComboBox, QListWidget, QListWidgetItem,
    QDialog, QHBoxLayout, QCheckBox
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon

class FileSystemHandler:
    """
    Cross-platform file system handler for PyOCR.
    Handles file selection and saving operations on Windows and Linux.
    """
    # Supported image file types
    IMAGE_TYPES = {
        "PNG Files": "*.png",
        "JPEG Files": "*.jpg *.jpeg",
        "TIFF Files": "*.tif *.tiff"
    }
    
    # Supported output file types
    OUTPUT_TYPES = {
        "Plain Text": "*.txt",
        "HTML (hOCR)": "*.html",
        "PDF": "*.pdf",
        "Text-only PDF": "*.pdf",
        "TSV": "*.tsv",
        "ALTO XML": "*.xml",
        "PAGE XML": "*.xml"
    }
    
    # Maps output format names to tesseract output format parameters
    OUTPUT_FORMAT_MAP = {
        "Plain Text": "txt",
        "HTML (hOCR)": "hocr",
        "PDF": "pdf",
        "Text-only PDF": "pdf",
        "TSV": "tsv",
        "ALTO XML": "alto",
        "PAGE XML": "page"
    }
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the file system handler.
        
        Args:
            parent: Parent widget for dialogs
        """
        self.parent = parent
        self.system = platform.system()
        self.recent_files: List[str] = []
        self.max_recent_files = 10
        self.last_directory = str(Path.home())
    
    def select_image_file(self) -> Optional[str]:
        """
        Open a file dialog to select an image file.
        
        Returns:
            Selected file path or None if canceled
        """
        # Create filter string for file dialog
        filters = []
        for name, pattern in self.IMAGE_TYPES.items():
            filters.append(f"{name} ({pattern})")
        
        # Add "All supported formats" option
        all_patterns = " ".join(pattern for pattern in self.IMAGE_TYPES.values())
        filters.insert(0, f"All supported images ({all_patterns})")
        
        # Add "All files" option
        filters.append("All files (*.*)")
        
        file_filter = ";;".join(filters)
        
        # Open file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Select Image File",
            self.last_directory,
            file_filter
        )
        
        if file_path:
            self.last_directory = str(Path(file_path).parent)
            self._add_to_recent_files(file_path)
            return file_path
        
        return None
    
    def select_output_file(self, default_format: str = "Plain Text") -> Optional[Tuple[str, str]]:
        """
        Open a file dialog to select where to save the output file.
        
        Args:
            default_format: Default output format
            
        Returns:
            Tuple of (file_path, format_name) or None if canceled
        """
        # Create filter string for file dialog
        filters = []
        for name, pattern in self.OUTPUT_TYPES.items():
            filters.append(f"{name} ({pattern})")
        
        file_filter = ";;".join(filters)
        selected_filter = f"{default_format} ({self.OUTPUT_TYPES[default_format]})"
        
        # Open file dialog
        file_path, selected_format = QFileDialog.getSaveFileName(
            self.parent,
            "Save Output As",
            self.last_directory,
            file_filter,
            selected_filter
        )
        
        if file_path:
            self.last_directory = str(Path(file_path).parent)
            
            # Extract format name from selected filter
            format_name = selected_format.split(" (")[0]
            
            # Ensure file has correct extension
            extension = self.OUTPUT_TYPES[format_name].replace("*", "").split()[0]
            if not file_path.lower().endswith(extension.lower()):
                file_path += extension
            
            return file_path, self.OUTPUT_FORMAT_MAP[format_name]
        
        return None
    
    def select_directory(self) -> Optional[str]:
        """
        Open a dialog to select a directory.
        
        Returns:
            Selected directory path or None if canceled
        """
        directory = QFileDialog.getExistingDirectory(
            self.parent,
            "Select Directory",
            self.last_directory,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if directory:
            self.last_directory = directory
            return directory
        
        return None
    
    def validate_file_type(self, file_path: str) -> bool:
        """
        Check if the file is one of the supported image types.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if file type is supported, False otherwise
        """
        if not file_path or not os.path.isfile(file_path):
            return False
            
        file_ext = Path(file_path).suffix.lower()
        
        # Check against all supported extensions
        for pattern in self.IMAGE_TYPES.values():
            extensions = pattern.split()
            for ext in extensions:
                if file_ext == ext.replace("*", ""):
                    return True
        
        return False
    
    def _add_to_recent_files(self, file_path: str) -> None:
        """
        Add a file to the recent files list.
        
        Args:
            file_path: Path to add to recent files
        """
        # Remove if already in list
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        
        # Add to beginning of list
        self.recent_files.insert(0, file_path)
        
        # Limit list size
        if len(self.recent_files) > self.max_recent_files:
            self.recent_files = self.recent_files[:self.max_recent_files]
    
    def get_recent_files(self) -> List[str]:
        """
        Get the list of recent files.
        
        Returns:
            List of recent file paths
        """
        return self.recent_files


class FileSelectionDialog(QDialog):
    """
    Enhanced file selection dialog with additional features.
    Provides a custom interface for selecting files with preview and recent files.
    """
    file_selected = pyqtSignal(str)
    
    def __init__(self, parent=None, file_handler=None):
        super().__init__(parent)
        self.file_handler = file_handler or FileSystemHandler(self)
        self.selected_file = None
        
        self.setWindowTitle("Select Image File")
        self.setMinimumSize(600, 400)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the dialog UI components"""
        layout = QVBoxLayout()
        
        # File type selection
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("File Type:"))
        
        self.type_combo = QComboBox()
        self.type_combo.addItem("All supported formats")
        for name in self.file_handler.IMAGE_TYPES.keys():
            self.type_combo.addItem(name)
        type_layout.addWidget(self.type_combo)
        
        layout.addLayout(type_layout)
        
        # Recent files list
        if self.file_handler.recent_files:
            layout.addWidget(QLabel("Recent Files:"))
            
            self.recent_list = QListWidget()
            for file_path in self.file_handler.recent_files:
                item = QListWidgetItem(Path(file_path).name)
                item.setData(Qt.ItemDataRole.UserRole, file_path)
                self.recent_list.addItem(item)
            
            self.recent_list.itemDoubleClicked.connect(self._on_recent_file_selected)
            layout.addWidget(self.recent_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._on_browse_clicked)
        button_layout.addWidget(browse_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def _on_browse_clicked(self):
        """Handle browse button click"""
        file_path = self.file_handler.select_image_file()
        if file_path:
            self.selected_file = file_path
            self.file_selected.emit(file_path)
            self.accept()
    
    def _on_recent_file_selected(self, item):
        """Handle selection from recent files list"""
        file_path = item.data(Qt.ItemDataRole.UserRole)
        if os.path.isfile(file_path):
            self.selected_file = file_path
            self.file_selected.emit(file_path)
            self.accept()
        else:
            QMessageBox.warning(
                self, 
                "File Not Found", 
                f"The file {file_path} no longer exists."
            )
            # Remove from recent files
            self.file_handler.recent_files.remove(file_path)
            self.recent_list.takeItem(self.recent_list.row(item))
    
    @classmethod
    def get_image_file(cls, parent=None, file_handler=None):
        """
        Static method to create and show the dialog.
        
        Args:
            parent: Parent widget
            file_handler: FileSystemHandler instance
            
        Returns:
            Selected file path or None if canceled
        """
        dialog = cls(parent, file_handler)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            return dialog.selected_file
        return None


class SaveFileDialog(QDialog):
    """
    Enhanced save file dialog with format selection.
    """
    def __init__(self, parent=None, file_handler=None):
        super().__init__(parent)
        self.file_handler = file_handler or FileSystemHandler(self)
        self.selected_file = None
        self.selected_format = "txt"
        
        self.setWindowTitle("Save Output")
        self.setMinimumSize(500, 300)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the dialog UI components"""
        layout = QVBoxLayout()
        
        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Output Format:"))
        
        self.format_combo = QComboBox()
        for name in self.file_handler.OUTPUT_TYPES.keys():
            self.format_combo.addItem(name)
        format_layout.addWidget(self.format_combo)
        
        layout.addLayout(format_layout)
        
        # Auto-copy checkbox
        self.auto_copy_cb = QCheckBox("Copy to clipboard after saving")
        layout.addWidget(self.auto_copy_cb)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save...")
        save_btn.clicked.connect(self._on_save_clicked)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def _on_save_clicked(self):
        """Handle save button click"""
        format_name = self.format_combo.currentText()
        result = self.file_handler.select_output_file(format_name)
        
        if result:
            self.selected_file, self.selected_format = result
            self.accept()
    
    @classmethod
    def get_save_location(cls, parent=None, file_handler=None):
        """
        Static method to create and show the dialog.
        
        Args:
            parent: Parent widget
            file_handler: FileSystemHandler instance
            
        Returns:
            Tuple of (file_path, format, auto_copy) or None if canceled
        """
        dialog = cls(parent, file_handler)
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            return (
                dialog.selected_file, 
                dialog.selected_format,
                dialog.auto_copy_cb.isChecked()
            )
        return None 
