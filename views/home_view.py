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
        image_layout.addWidget(
            img_label, alignment=Qt.AlignCenter
        )
        layout.addLayout(image_layout)
        layout.addSpacing(20)

        text_label = QLabel(
            "The chess tournament manager "
            "that supports your events."
        )
        text_label.setObjectName("home-text")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        text_layout = QHBoxLayout()
        text_layout.addWidget(
            text_label, alignment=Qt.AlignCenter
        )
        layout.addLayout(text_layout)

        self.setLayout(layout)
