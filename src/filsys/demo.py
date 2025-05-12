#!/usr/bin/env python3
"""
Demo for the cross-platform file system handler.
Shows how to use the file selection and save dialogs.
"""

import sys
from pathlib import Path

# Add parent directory to path to allow importing from src
sys.path.append(str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit
from PyQt6.QtCore import Qt

from src.filsys.file_handler import FileSystemHandler, FileSelectionDialog, SaveFileDialog


class FileSystemDemo(QMainWindow):
    """Demo application for the file system handler."""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("File System Handler Demo")
        self.setMinimumSize(600, 400)
        
        self.file_handler = FileSystemHandler(self)
        self.selected_file = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the UI components."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel("File System Handler Demo")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # File selection buttons
        select_file_btn = QPushButton("Select Image File")
        select_file_btn.clicked.connect(self._on_select_file_clicked)
        layout.addWidget(select_file_btn)
        
        select_file_enhanced_btn = QPushButton("Select Image File (Enhanced Dialog)")
        select_file_enhanced_btn.clicked.connect(self._on_select_file_enhanced_clicked)
        layout.addWidget(select_file_enhanced_btn)
        
        select_dir_btn = QPushButton("Select Directory")
        select_dir_btn.clicked.connect(self._on_select_dir_clicked)
        layout.addWidget(select_dir_btn)
        
        save_file_btn = QPushButton("Save Output")
        save_file_btn.clicked.connect(self._on_save_file_clicked)
        layout.addWidget(save_file_btn)
        
        save_file_enhanced_btn = QPushButton("Save Output (Enhanced Dialog)")
        save_file_enhanced_btn.clicked.connect(self._on_save_file_enhanced_clicked)
        layout.addWidget(save_file_enhanced_btn)
        
        # Results display
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)
        
        central_widget.setLayout(layout)
    
    def _on_select_file_clicked(self):
        """Handle select file button click."""
        file_path = self.file_handler.select_image_file()
        if file_path:
            self.selected_file = file_path
            self._log_result(f"Selected file: {file_path}")
            
            # Validate file type
            if self.file_handler.validate_file_type(file_path):
                self._log_result("File type is valid")
            else:
                self._log_result("File type is not supported")
    
    def _on_select_file_enhanced_clicked(self):
        """Handle enhanced select file button click."""
        file_path = FileSelectionDialog.get_image_file(self, self.file_handler)
        if file_path:
            self.selected_file = file_path
            self._log_result(f"Selected file (enhanced): {file_path}")
    
    def _on_select_dir_clicked(self):
        """Handle select directory button click."""
        directory = self.file_handler.select_directory()
        if directory:
            self._log_result(f"Selected directory: {directory}")
    
    def _on_save_file_clicked(self):
        """Handle save file button click."""
        result = self.file_handler.select_output_file()
        if result:
            file_path, format_name = result
            self._log_result(f"Save location: {file_path}")
            self._log_result(f"Format: {format_name}")
    
    def _on_save_file_enhanced_clicked(self):
        """Handle enhanced save file button click."""
        result = SaveFileDialog.get_save_location(self, self.file_handler)
        if result:
            file_path, format_name, auto_copy = result
            self._log_result(f"Save location (enhanced): {file_path}")
            self._log_result(f"Format: {format_name}")
            self._log_result(f"Auto-copy: {auto_copy}")
    
    def _log_result(self, message):
        """Add a message to the results text area."""
        self.results_text.append(message)


def main():
    """Main entry point for the demo."""
    app = QApplication(sys.argv)
    
    # Apply stylesheet
    app.setStyleSheet("""
        QMainWindow, QDialog {
            background-color: #2d2d2d;
        }
        QWidget {
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #3a3a3a;
            border: 1px solid #5a5a5a;
            padding: 5px 10px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #4a4a4a;
        }
        QTextEdit {
            background-color: #1d1d1d;
            border: 1px solid #5a5a5a;
        }
        QLabel {
            color: #e0e0e0;
        }
        QComboBox {
            background-color: #3a3a3a;
            border: 1px solid #5a5a5a;
            padding: 3px;
        }
        QListWidget {
            background-color: #1d1d1d;
            border: 1px solid #5a5a5a;
        }
    """)
    
    window = FileSystemDemo()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 