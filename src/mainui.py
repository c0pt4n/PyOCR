import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QGridLayout, QWidget, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QSlider, QVBoxLayout, QGroupBox, QRadioButton, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon

# Custom modules
from filsys.file_handler import FileSystemHandler, FileSelectionDialog
from img_enhance.enhancer import ImageEnhancer, EnhancementParams
from ocrMod.ocr_engine import OCREngine

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
    process_layout = QVBoxLayout()
    
    # Mode selection group
    mode_group = QGroupBox("Processing Mode")
    mode_group.setStyleSheet(f"""
        QGroupBox {{
            color: {TEXT_PRIMARY_COLOR};
            border: 1px solid {TEXTBOX_BORDER};
            border-radius: 4px;
            margin-top: 12px;
            padding-top: 8px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
    """)
    
    mode_layout = QVBoxLayout(mode_group)
    
    # Radio buttons for auto/manual
    auto_radio = QRadioButton("Auto")
    manual_radio = QRadioButton("Manual")
    auto_radio.setChecked(True)  # Default to auto
    
    auto_radio.setStyleSheet(f"""
        QRadioButton {{
            color: {TEXT_PRIMARY_COLOR};
            spacing: 6px;
        }}
        QRadioButton::indicator {{
            width: 14px;
            height: 14px;
            border-radius: 7px;
            border: 1px solid {TEXTBOX_BORDER};
        }}
        QRadioButton::indicator:checked {{
            background-color: {PRIMARY_BUTTON_BG};
            border: 1px solid {PRIMARY_BUTTON_BG};
        }}
    """)
    manual_radio.setStyleSheet(auto_radio.styleSheet())
    
    mode_layout.addWidget(auto_radio)
    mode_layout.addWidget(manual_radio)
    
    process_layout.addWidget(mode_group)
    
    # Enhancement options - initially hidden, shown in manual mode
    enhance_options = QGroupBox("Image Enhancement")
    enhance_options.setStyleSheet(mode_group.styleSheet())
    enhance_options.setVisible(False)  # Initially hidden for auto mode
    
    enhance_layout = QVBoxLayout(enhance_options)
    
    # Enhancement sliders
    brightness_label = QLabel("Brightness:")
    brightness_slider = QSlider(Qt.Orientation.Horizontal)
    brightness_slider.setRange(50, 150)
    brightness_slider.setValue(100)  # Default 1.0
    
    contrast_label = QLabel("Contrast:")
    contrast_slider = QSlider(Qt.Orientation.Horizontal)
    contrast_slider.setRange(50, 200)
    contrast_slider.setValue(100)  # Default 1.0
    
    sharpness_label = QLabel("Sharpness:")
    sharpness_slider = QSlider(Qt.Orientation.Horizontal)
    sharpness_slider.setRange(0, 200)
    sharpness_slider.setValue(100)  # Default 1.0
    
    # Checkbox options
    denoise_check = QCheckBox("Denoise")
    binarize_check = QCheckBox("Binarize")
    deskew_check = QCheckBox("Deskew")
    
    slider_style = f"""
        QSlider::groove:horizontal {{
            height: 6px;
            background: {TEXTBOX_BORDER};
            border-radius: 3px;
        }}
        QSlider::handle:horizontal {{
            background: {PRIMARY_BUTTON_BG};
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }}
        QSlider::sub-page:horizontal {{
            background: {PRIMARY_BUTTON_BG};
            border-radius: 3px;
        }}
    """
    
    checkbox_style = f"""
        QCheckBox {{
            color: {TEXT_PRIMARY_COLOR};
            spacing: 6px;
        }}
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 1px solid {TEXTBOX_BORDER};
            border-radius: 3px;
        }}
        QCheckBox::indicator:checked {{
            background-color: {PRIMARY_BUTTON_BG};
            border: 1px solid {PRIMARY_BUTTON_BG};
        }}
    """
    
    brightness_slider.setStyleSheet(slider_style)
    contrast_slider.setStyleSheet(slider_style)
    sharpness_slider.setStyleSheet(slider_style)
    denoise_check.setStyleSheet(checkbox_style)
    binarize_check.setStyleSheet(checkbox_style)
    deskew_check.setStyleSheet(checkbox_style)
    
    enhance_layout.addWidget(brightness_label)
    enhance_layout.addWidget(brightness_slider)
    enhance_layout.addWidget(contrast_label)
    enhance_layout.addWidget(contrast_slider)
    enhance_layout.addWidget(sharpness_label)
    enhance_layout.addWidget(sharpness_slider)
    enhance_layout.addWidget(denoise_check)
    enhance_layout.addWidget(binarize_check)
    enhance_layout.addWidget(deskew_check)
    
    process_layout.addWidget(enhance_options)
    
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
    process_layout.addWidget(process_button, alignment=Qt.AlignmentFlag.AlignCenter)
    
    # Add the entire process layout to the main layout
    layout.addLayout(process_layout, 2, 0, alignment=Qt.AlignmentFlag.AlignCenter)

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

    def toggle_enhance_options():
        enhance_options.setVisible(manual_radio.isChecked())
    
    auto_radio.toggled.connect(toggle_enhance_options)
    manual_radio.toggled.connect(toggle_enhance_options)
    
    # Create instances of our processing modules
    img_enhancer = ImageEnhancer()
    ocr_engine = OCREngine()
    
    def process_action():
        image_path = text_box.text()
        if not image_path:
            output.setText("Please select an image first.")
            return
        
        try:
            # Configure enhancement parameters based on mode
            if auto_radio.isChecked():
                # Auto mode uses default parameters
                params = EnhancementParams(
                    brightness=1.1,  # Slight brightness increase
                    contrast=1.2,    # Moderate contrast increase
                    sharpness=1.2,   # Moderate sharpness increase
                    denoise=True,    # Enable denoising
                    binarize=True    # Enable binarization
                )
            else:
                # Manual mode uses slider values
                params = EnhancementParams(
                    brightness=brightness_slider.value() / 100.0,
                    contrast=contrast_slider.value() / 100.0,
                    sharpness=sharpness_slider.value() / 100.0,
                    denoise=denoise_check.isChecked(),
                    binarize=binarize_check.isChecked(),
                    deskew=deskew_check.isChecked()
                )
            
            # Update enhancer with our parameters
            img_enhancer.set_params(params)
            
            # Process and enhance the image
            output.setText(f"Enhancing image: {image_path}...")
            enhanced_image = img_enhancer.enhance(image_path)
            
            # Perform OCR on the enhanced image
            output.setText(output.toPlainText() + "\nExtracting text...")
            ocr_result = ocr_engine.process_pil_image(enhanced_image)
            
            # Display the final result
            output.setText(f"OCR Result:\n\n{ocr_result}")
            
        except Exception as e:
            output.setText(f"Error processing image: {str(e)}")

    process_button.clicked.connect(process_action)

    central_widget.setLayout(layout)

    window.show()
    sys.exit(app.exec())
