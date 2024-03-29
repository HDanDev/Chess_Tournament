from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt
from controllers.tournament_controller import TournamentController
from repositories.player_repository import PlayerRepository
from views.partials.date_delegate import DateDelegate

# from views.partials.int_delegate import IntDelegate


class TournamentSimulatorView(QWidget):
    def __init__(self, nav, tournament):
        super().__init__()

        self.nav = nav
        self.tournament_controller = TournamentController(nav, tournament)
        self.tournament = tournament
        self.player_repository = PlayerRepository()
        self.date_delegate = DateDelegate(self)
        # self.int_delegate = IntDelegate(self)
        self.all_players = self.player_repository.read_json()
        self.id_index_column = 3

        self.layout = QVBoxLayout()

        self.label = QLabel("Tournament Simulator")
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Player", "Score"])
        self.table.setVisible(False)

        self.layout.addWidget(self.table)

        # self.selected_players_table = None

        self.setLayout(self.layout)

        # self.tournament_controller.save_new_item(self.tournament)
        self.tournament_controller.setup_view(self)

    def populate_table(self):
        for i in range(
            len(self.tournament.rounds),
            int(self.tournament.num_rounds)
        ):
            current_round = (
                int(i)
                if (
                    len(self.tournament.rounds)
                    == int(self.tournament.num_rounds)
                )
                else int(i) + 1
            )
            print(
                f"self.tournament.num_rounds : {self.tournament.num_rounds}"
                )
            print(f"i : {i}")
            print(f"currentround : {current_round}")
            print(f"length : {len(self.tournament.rounds)}")
            self.tournament_controller.generate_pairs(
                current_round=int(current_round), is_simulation=True
            )
            self.create_round_table(self.tournament.rounds[int(i)])

        self.message = QLabel("Tournament is over")
        self.message.setAlignment(Qt.AlignHCenter)
        self.message.setObjectName("error")
        self.layout.addWidget(self.message)

        self.view_round_button = QPushButton("Go to results")
        self.view_round_button.clicked.connect(self.see_rounds)
        self.layout.addWidget(self.view_round_button)
        self.layout.addStretch()

    def create_round_table(self, round):
        title = QLabel(
            f"Round \"{round.name}\" ended at "
            f"{round.end_datetime.toString('dddd, yyyy-MM-dd HH:mm:ss')}"
        )
        round_table = QTableWidget()
        round_table.setColumnCount(2)
        round_table.setHorizontalHeaderLabels(["Matches", "Winner"])

        for match in round.matches:
            row_position = round_table.rowCount()
            round_table.insertRow(row_position)

            matches_item = QTableWidgetItem(
                f"{match.player1.get_full_name()} "
                f"vs {match.player2.get_full_name()}"
            )
            matches_item.setFlags(matches_item.flags() & ~Qt.ItemIsEditable)
            round_table.setItem(row_position, 0, matches_item)

            result = QTableWidgetItem(f"{match.get_winner()}")
            result.setFlags(result.flags() & ~Qt.ItemIsEditable)
            round_table.setItem(row_position, 1, result)

        self.resize_table_to_content(round_table)

        self.layout.addWidget(title)
        self.layout.addWidget(round_table)

        self.layout.addWidget(round_table)

    def resize_table_to_content(self, table):
        total_height = table.horizontalHeader().height()
        for row in range(table.rowCount()):
            total_height += table.rowHeight(row)

        table.setFixedHeight(total_height)

    def see_rounds(self):
        self.nav.switch_to_rounds_read(self.tournament)
