import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QGridLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

# Custom modules
from filsys.file_handler import FileSystemHandler, FileSelectionDialog

# --- Cyberpunk Neon Palette ---
# Core Colors
BACKGROUND_COLOR = "#0A0F14"  # Space Black (softer than pure black)
TEXT_PRIMARY_COLOR = "#E0E3E7"  # Cool Mist White (better readability)

# Text Boxes
TEXTBOX_BG = "#1A1F27"        # Deep Space
TEXTBOX_BORDER = "#3B4251"    # Cyber Gray
TEXTBOX_FOCUS = "#5AD9FF"     # Neo-Cyan
TEXTBOX_HOVER = "#4A90E2"     # Electric Blue

# Buttons
PRIMARY_BUTTON_BG = "#00B4D8"  # Tech Cyan (softer than electric)
PRIMARY_BUTTON_TEXT = "#0A0F14" # Contrast Dark
SECONDARY_BUTTON_BG = "#3B4251" # Cyber Gray
SUCCESS_BUTTON_BG = "#2ECC71"   # Matrix Green
DANGER_BUTTON_BG = "#FF6B6B"    # Alert Coral

# States
HOVER_STATE = "#0096C7"        # Deep Cyan
ACTIVE_STATE = "#0077B6"       # Ocean Blue
DISABLED_STATE = "#2D3748"     # Steel Gray
# -----------------------------

def mainui():
    app = QApplication(sys.argv)

    app.setStyleSheet(f"""
        QMainWindow {{
            background-color: {BACKGROUND_COLOR};
        }}
        QWidget {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_PRIMARY_COLOR};
        }}
        QLabel {{
            color: {TEXT_PRIMARY_COLOR};
            background-color: transparent;
        }}
        QLineEdit {{
            background-color: {TEXTBOX_BG};
            border: 2px solid {TEXTBOX_BORDER};
            color: {TEXT_PRIMARY_COLOR};
            padding: 8px;
            border-radius: 4px;
            font-size: 14px;
        }}
        QLineEdit:focus {{
            border-color: {TEXTBOX_FOCUS};
        }}
        QPushButton {{
            background-color: {SECONDARY_BUTTON_BG};
            color: {TEXT_PRIMARY_COLOR};
            border: 1px solid {TEXTBOX_BORDER};
            padding: 8px 16px;
            border-radius: 4px;
            min-width: 80px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {HOVER_STATE};
            border-color: {TEXTBOX_FOCUS};
        }}
        QPushButton:pressed {{
            background-color: {ACTIVE_STATE};
        }}
        QTextEdit {{
            background-color: {BACKGROUND_COLOR};
            border: 1px solid {TEXTBOX_BORDER};
            color: {TEXT_PRIMARY_COLOR};
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
        }}
    """)
    # --- End Stylesheet ---

    # Project root directory
    project_root = Path(__file__).parent.parent

    window = QMainWindow()
    window.setWindowTitle("PyOCR")
    window.resize(400, 300) # width, height

    # Set the favicon (window icon)
    favicon_path = project_root / "assets" / "favicon.png"
    window.setWindowIcon(QIcon(str(favicon_path)))

    central_widget = QWidget()
    window.setCentralWidget(central_widget)

    layout = QGridLayout()
    layout.setContentsMargins(20, 20, 20, 20)

    # Load logo with absolute path
    logo_path = project_root / "assets" / "logo.png"
    pixmap = QPixmap(str(logo_path)).scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio)

    logo_label = QLabel()
    logo_label.setPixmap(pixmap)
    logo_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    # Syntax: layout.addWidget(widget, row, column, [rowSpan, columnSpan])
    layout.addWidget(logo_label, 0, 0)

    # Input Row (TextBox + Button)
    input_layout = QHBoxLayout()
    text_box = QLineEdit()
    text_box.setReadOnly(True)
    text_box.setPlaceholderText("Select an image...")
    text_box.setFixedSize(300, 40)
    text_box.setStyleSheet(f"""
        QLineEdit {{
            background-color: {TEXTBOX_BG};
            border: 2px solid {TEXTBOX_BORDER};
            color: {TEXT_PRIMARY_COLOR};
            padding: 8px;
            border-radius: 4px;
        }}
        QLineEdit:focus {{
            border-color: {TEXTBOX_FOCUS};
        }}
    """)
    input_layout.addWidget(text_box)

    file_handler = FileSystemHandler(window)
    def select_file():
        # Use the custom file selection dialog
        file_path = FileSelectionDialog.get_image_file(window, file_handler)
        if file_path:
            text_box.setText(file_path)
            # Optional: Add to recent files through handler
            file_handler._add_to_recent_files(file_path)

    select_button = QPushButton("Select")
    select_button.setFixedSize(110, 30)
    select_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {PRIMARY_BUTTON_BG};
            color: {PRIMARY_BUTTON_TEXT};
            border: none;
            padding: 8px 16px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {HOVER_STATE};
        }}
        QPushButton:pressed {{
            background-color: {ACTIVE_STATE};
        }}
    """)
    select_button.clicked.connect(select_file)
    input_layout.addWidget(select_button)

    layout.addLayout(input_layout, 1, 0)

    # Process Button
    process_button = QPushButton("Process")
    process_button.setFixedSize(110, 30)
    process_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {SUCCESS_BUTTON_BG};
            color: {BACKGROUND_COLOR};
            border: none;
            padding: 8px 16px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: #25A35A;  /* Darker shade of success */
        }}
        QPushButton:pressed {{
            background-color: #1E8449;  /* Even darker shade */
        }}
    """)
    layout.addWidget(process_button, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)

    # Output Terminal
    output = QTextEdit()
    output.setReadOnly(True)
    output.setFixedSize(400, 200)
    output.setStyleSheet(f"""
        QTextEdit {{
            background-color: {BACKGROUND_COLOR};
            border: 1px solid {TEXTBOX_BORDER};
            color: {TEXT_PRIMARY_COLOR};
            padding: 10px;
            font-family: monospace;
        }}
    """)
    output.setText("the output terminal")
    layout.addWidget(output, 3, 0, alignment=Qt.AlignmentFlag.AlignCenter)

    def process_action():
        if text_box.text():
            output.setText(f"Processing: {text_box.text()}")
        else:
            output.setText("Please select an image first.")

    process_button.clicked.connect(process_action)

    central_widget.setLayout(layout)

    window.show()
    sys.exit(app.exec())
