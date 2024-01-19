from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from views.partials.input_field import InputField, FormType
from models.player import Player
from repositories.player_repository import PlayerRepository


class PlayerCreationView(QWidget):
    def __init__(self, nav):
        super().__init__()

        self.nav = nav
        self.player_repository = PlayerRepository()

        self.layout = QVBoxLayout()

        self.label = QLabel("Registration Form")
        self.layout.addWidget(self.label)

        self.first_name = InputField(
            self.layout,
            "First name*",
            "Player's first name",
            is_mandatory=True
        )
        self.last_name = InputField(
            self.layout,
            "Last name*",
            "Player's last name",
            is_mandatory=True
        )
        self.date_of_birth = InputField(
            self.layout,
            "Birth date",
            "Player's date of birth",
            FormType.Date
        )
        self.chess_id = InputField(
            self.layout,
            "Chess ID",
            ('Player\'s chess ID must be in "XX00000" format, '
             'if left empty an ID will be automatically generated'),
            is_regex=True,
        )

        self.message = QLabel()

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)

        self.layout.addWidget(self.message)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def register(self):
        if (
            self.first_name.validate_input()
            and self.last_name.validate_input()
        ):
            new_player = Player()

            new_player.first_name = self.first_name.input.text()
            new_player.last_name = self.last_name.input.text()
            new_player.date_of_birth = self.date_of_birth.input.date()
            new_player.chess_id = self.chess_id.input.text()

            try:
                self.player_repository.add_json(new_player)
            except ValueError as e:
                self.message.setText("Error:", e)
                self.message.setObjectName(
                    "color: #fd3c35; font-weight: bold;"
                    )
                print("Error:", e)
            else:
                self.message.setText(
                    f"Successfully added player {new_player.get_full_name()}"
                )
                self.message.setStyleSheet(
                    "color: #269add; font-weight: bold;"
                    )
                print(
                    f"Successfully added player {new_player.get_full_name()}"
                    )
        else:
            self.last_name.validate_input()
