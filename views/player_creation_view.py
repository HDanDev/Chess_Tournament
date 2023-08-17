from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

class PlayerCreationView(QWidget):
    def __init__(self, app):
        super().__init__()

        self.app = app

        self.layout = QVBoxLayout(self)
        self.label = QLabel("Player creation", self)
        self.layout.addWidget(self.label)
