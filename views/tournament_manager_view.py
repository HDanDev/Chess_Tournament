from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt, QDateTime
from views.partials.input_field import InputField, FormType
from models.tournament import Tournament
from controllers.tournament_controller import TournamentController
from views.partials.date_delegate import DateDelegate
from views.partials.int_delegate import IntDelegate

class TournamentManagerView(QWidget):
    def __init__(self, nav, tournament):
        super().__init__()

        self.nav = nav
        self.tournament_controller = TournamentController(nav, tournament)
        self.tournament = tournament
        self.date_delegate = DateDelegate(self)
        self.int_delegate = IntDelegate(self)

        self.layout = QVBoxLayout()

        self.label = QLabel("Tournament Manager")
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Name", "Location", "Starting date", "Ending date", "Number of rounds", "remarks"])
        self.table.setColumnHidden(6, True) 

        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        
        self.tournament_controller.save_new_item(self.tournament)
        self.tournament_controller.setup_view(self)

    def populate_table(self, tournament):        
        id = QTableWidgetItem(tournament.id)
        id.setFlags(id.flags() & ~Qt.ItemIsEnabled)
        # self.table.setItemDelegateForColumn(2, self.date_delegate)
        # self.table.setItemDelegateForColumn(3, self.date_delegate)
        self.table.setItemDelegateForColumn(4, self.int_delegate)

        name = QTableWidgetItem(tournament.name)
        location = QTableWidgetItem(tournament.location)

        start_date = QTableWidgetItem(tournament.start_date.toString(Qt.ISODate))
        start_date.setData(Qt.DisplayRole, start_date.text())
        start_date.setData(Qt.EditRole, tournament.start_date)

        end_date = QTableWidgetItem(tournament.end_date.toString(Qt.ISODate))
        end_date.setData(Qt.DisplayRole, end_date.text())
        end_date.setData(Qt.EditRole, tournament.end_date)

        num_rounds = QTableWidgetItem(str(tournament._num_rounds))
        num_rounds.setData(Qt.EditRole, int(tournament._num_rounds))

        remarks = QTableWidgetItem(tournament.remarks)
                
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, name)
        self.table.setItem(row_position, 1, location)
        self.table.setItem(row_position, 2, start_date)
        self.table.setItem(row_position, 3, end_date)
        self.table.setItem(row_position, 4, num_rounds)
        self.table.setItem(row_position, 5, remarks)
        self.table.setItem(row_position, 6, id)
        
        self.table.itemChanged.connect(self.handle_item_changed)
        
    def handle_item_changed(self, item):
        row = item.row()
        try: 
            id_item = self.table.item(row, 6) 
            tournament_id = id_item.text()
            edited_tournament = Tournament(
                id=tournament_id,
                name=self.table.item(row, 0).text(),
                location=self.table.item(row, 1).text(),
                start_date=QDateTime.fromString(self.table.item(row, 2).text(), Qt.ISODate),
                end_date=QDateTime.fromString(self.table.item(row, 3).text(), Qt.ISODate),
                num_rounds=int(self.table.item(row, 4).text()),
                remarks=self.table.item(row, 5).text()
            )
            self.tournament_controller.save_changes(edited_tournament)
        except Exception as e:
            print(f"Error fnding item: {e}")   