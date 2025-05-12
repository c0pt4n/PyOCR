import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QGridLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

# --- Cyberpunk Neon Palette ---
BACKGROUND_COLOR = "#000000"  # Deep Black
PRIMARY_COLOR = "#00FFFF"     # Electric Cyan (for the H1 title)
TEXT_PRIMARY_COLOR = "#C0C0C0" # Light Gray/Silver (for potential future default text)
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

    central_widget.setLayout(layout)

    window.show()
    sys.exit(app.exec())
