import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QGridLayout, QWidget,
    QPushButton, QFileDialog, QTextEdit, QHBoxLayout, QVBoxLayout, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

# --- Cyberpunk Neon Palette ---
BACKGROUND_COLOR = "#000000"  # Deep Black
PRIMARY_COLOR = "#00FFFF"     # Electric Cyan
TEXT_PRIMARY_COLOR = "#C0C0C0" # Light Gray/Silver
GRADIENT_LEFT = "#7e57ff"
GRADIENT_RIGHT = "#5ad9ff"
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
        QPushButton {{
            background-color: transparent;
            border: 1px solid {PRIMARY_COLOR};
            color: {PRIMARY_COLOR};
            padding: 5px;
        }}
        QPushButton:hover {{
            background-color: {PRIMARY_COLOR};
            color: {BACKGROUND_COLOR};
        }}
    """)

    # Project root directory
    project_root = Path(__file__).parent.parent

    window = QMainWindow()
    window.setWindowTitle("PyOCR")
    window.resize(400, 300)

    # Set the favicon (window icon)
    favicon_path = project_root / "assets" / "favicon.png"
    window.setWindowIcon(QIcon(str(favicon_path)))

    # Central widget & layout
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QGridLayout()
    layout.setContentsMargins(20, 20, 20, 20)

    # Logo
    logo_path = project_root / "assets" / "logo.png"
    pixmap = QPixmap(str(logo_path)).scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio)
    
    logo_label = QLabel()
    logo_label.setPixmap(pixmap)
    logo_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(logo_label, 0, 0)

    # Input Row (TextBox + Button)
    input_layout = QHBoxLayout()
    text_box = QLineEdit()
    text_box.setReadOnly(True)
    text_box.setPlaceholderText("Select an image...")
    text_box.setFixedSize(300, 40)
    text_box.setStyleSheet(f"""
        QLineEdit {{
            background-color: {GRADIENT_LEFT};
            color: white;
            padding: 5px;
            border-radius: 5px;
            font-size: 13px;
        }}
    """)
    input_layout.addWidget(text_box)

    def select_file():
        file_path, _ = QFileDialog.getOpenFileName(window, "Select Image", "", "Images (*.png)")
        if file_path:
            text_box.setText(file_path)

    select_button = QPushButton("Select")
    select_button.setFixedSize(110, 30)
    select_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {GRADIENT_RIGHT};
            color: black;
            border: none;
            padding: 8px;
            font-size: 11px;
            border-radius: 5px;
        }}
    """)
    select_button.clicked.connect(select_file)
    input_layout.addWidget(select_button)

    layout.addLayout(input_layout, 1, 0)

    # Process Button
    process_button = QPushButton("Process")
    process_button.setFixedSize(110, 30)
    process_button.setStyleSheet("""
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #9c51ff, stop:1 #0dc668);
            color: white;
            border: none;
            font-size: 11px;
            border-radius: 4px;
        }
    """)
    layout.addWidget(process_button, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)

    # Output Terminal
    output = QTextEdit()
    output.setReadOnly(True)
    output.setFixedSize(400, 200)
    output.setStyleSheet("""
        background-color: #2be2c4;
        color: white;
        font-size: 13px;
        border: none;
        padding: 10px;
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


if __name__ == "__main__":
    mainui()
