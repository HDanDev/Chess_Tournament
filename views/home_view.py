from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtGui import QPixmap

class HomeView(QWidget):
    def __init__(self, main_app):
        super().__init__()

        self.main_app = main_app
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        img_label = QLabel(self)
        img_label.setObjectName("img")
        pixmap = QPixmap("./assets/img/chess_img.png")
        img_label.setPixmap(pixmap)
        image_layout = QHBoxLayout()
        img_label.setScaledContents(True)
        image_layout.addWidget(img_label, alignment=Qt.AlignCenter)  # Center the content horizontally
        layout.addLayout(image_layout)
        layout.addSpacing(20)
        
        text_label = QLabel("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
        text_label.setObjectName("home-text")
        text_label.setAlignment(Qt.AlignCenter)  # Center the content horizontally
        text_label.setWordWrap(True)  # Enable word wrapping for the text
        text_layout = QHBoxLayout()
        text_layout.addWidget(text_label, alignment=Qt.AlignCenter)  # Center the content horizontally
        layout.addLayout(text_layout)
        
        self.setLayout(layout)
