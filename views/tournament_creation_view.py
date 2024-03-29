from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget
from views.partials.input_field import InputField, FormType
from models.tournament import Tournament
from controllers.tournament_controller import TournamentController


class TournamentCreationView(QWidget):
    def __init__(self, nav):
        super().__init__()

        self._nav = nav
        self._tournament_controller = TournamentController(self._nav)

        self.layout = QVBoxLayout()

        self.label = QLabel("Registration Form")
        self.layout.addWidget(self.label)

        self.name = InputField(self.layout, "Name", "Tournament name")
        self.location = InputField(self.layout, "Location", "Location name")
        self.start_date = InputField(
            self.layout, "Start date", "Starting date", FormType.DateTime
        )
        self.end_date = InputField(
            self.layout, "End date", "Ending date", FormType.DateTime
        )
        self._num_rounds = InputField(
            self.layout, "Number of rounds",
            "Number of rounds",
            FormType.Numerical
        )
        # self.players = InputField(self.layout,
        # "Registered player",
        # "Registered player",
        # FormType.Combo)
        self.remarks = InputField(self.layout,
                                  "Remarks",
                                  "Remarks",
                                  FormType.LongText
                                  )

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)
        self.layout.addWidget(self.register_button)

        self.setLayout(self.layout)

    def register(self):
        new_tournament = Tournament()
        if self.name.input.text():
            new_tournament.name = self.name.input.text()
        if self.location.input.text():
            new_tournament.location = self.location.input.text()
        # location=self.location.currentText()/currentData(),
        # ### That is if location is a combo box
        new_tournament.start_date = self.start_date.input.dateTime()
        new_tournament.end_date = self.end_date.input.dateTime()
        if self._num_rounds.input.text():
            new_tournament.num_rounds = self._num_rounds.input.text()
        new_tournament.remarks = self.remarks.input.toPlainText()

        self._tournament_controller.save_new_item(new_tournament)
        self._nav.switch_to_tournament_manager(new_tournament)
