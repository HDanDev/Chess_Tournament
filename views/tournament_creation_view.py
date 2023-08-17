from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from views.partials.input_field import InputField

class TournamentCreationView(QWidget):
    def __init__(self, main_app):
        super().__init__()

        self.main_app = main_app

        self.layout = QVBoxLayout()

        self.label = QLabel("Registration Form")
        self.layout.addWidget(self.label)

        self.username_field = InputField(self.layout, "username", "test")
        self.password_field = InputField(self.layout, "password", "test")
        self.ok_field = InputField(self.layout, "else", "test")

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Perform registration logic here

        # Switch to another view (e.g., View2)
        self.main_app.switch_to_home()