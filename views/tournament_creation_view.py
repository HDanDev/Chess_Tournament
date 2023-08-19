from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from views.partials.input_field import InputField, FormType
from models.tournament import Tournament

class TournamentCreationView(QWidget):
    def __init__(self, nav):
        super().__init__()

        self.nav = nav

        self.layout = QVBoxLayout()

        self.label = QLabel("Registration Form")
        self.layout.addWidget(self.label)

        self.name = InputField(self.layout, "Name", "Tournament name")
        self.location = InputField(self.layout, "Location", "Location name")
        self.start_date = InputField(self.layout, "Start date", "Starting date", FormType.Date)
        self.end_date = InputField(self.layout, "End date", "Ending date", FormType.Date)
        self._num_rounds = InputField(self.layout, "Number of rounds", "Number of rounds", FormType.Numerical)
        self.players = InputField(self.layout, "Registered player", "Registered player", FormType.Combo)
        self.remarks = InputField(self.layout, "Remarks", "Remarks", FormType.LongText)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def register(self):
        new_tournament = Tournament(
            name=self.name.input.text(),
            location=self.location.input.text(),
            # location=self.location.currentText()/currentData(), ### That is if location is a combo box
            start_date=self.start_date.input.dateTime(),
            end_date=self.end_date.input.dateTime(),
            num_rounds=self._num_rounds.input.text(),
            remarks=self.remarks.input.toPlainText()
        )
        
        self.nav.switch_to_tournament_manager(new_tournament)