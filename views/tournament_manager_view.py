from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QDialog, QCheckBox
from PySide6.QtCore import Qt, QDateTime
from views.partials.input_field import InputField, FormType
from models.tournament import Tournament
from controllers.tournament_controller import TournamentController
from views.partials.date_delegate import DateDelegate
from views.partials.int_delegate import IntDelegate
from views.partials.centered_check_box_widget import CenteredCheckBoxWidget

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
        
        self.selected_players_table = None

        self.setLayout(self.layout)
        
        self.tournament_controller.save_new_item(self.tournament)
        self.tournament_controller.setup_view(self)

    def populate_table(self):        
        id = QTableWidgetItem(self.tournament.id)
        id.setFlags(id.flags() & ~Qt.ItemIsEnabled)
        # self.table.setItemDelegateForColumn(2, self.date_delegate)
        # self.table.setItemDelegateForColumn(3, self.date_delegate)
        self.table.setItemDelegateForColumn(4, self.int_delegate)

        name = QTableWidgetItem(self.tournament.name)
        location = QTableWidgetItem(self.tournament.location)

        start_date = QTableWidgetItem(self.tournament.start_date.toString(Qt.ISODate))
        start_date.setData(Qt.DisplayRole, start_date.text())
        start_date.setData(Qt.EditRole, self.tournament.start_date)

        end_date = QTableWidgetItem(self.tournament.end_date.toString(Qt.ISODate))
        end_date.setData(Qt.DisplayRole, end_date.text())
        end_date.setData(Qt.EditRole, self.tournament.end_date)

        num_rounds = QTableWidgetItem(str(self.tournament._num_rounds))
        num_rounds.setData(Qt.EditRole, int(self.tournament._num_rounds))

        remarks = QTableWidgetItem(self.tournament.remarks)
                
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, name)
        self.table.setItem(row_position, 1, location)
        self.table.setItem(row_position, 2, start_date)
        self.table.setItem(row_position, 3, end_date)
        self.table.setItem(row_position, 4, num_rounds)
        self.table.setItem(row_position, 5, remarks)
        self.table.setItem(row_position, 6, id)
        
        self.resize_table_to_content()
        self.table.itemChanged.connect(self.handle_item_changed)        
        
        self.save_players_button = QPushButton("Save changes")
        self.save_players_button.clicked.connect(self.save_selected_players)
        self.save_players_button.setVisible(False)
        
        self.manually_add_players_btn = QPushButton("Manually add players")
        self.manually_add_players_btn.clicked.connect(self.toggle_selected_players_table)
        self.layout.addWidget(self.manually_add_players_btn)
        
        
        self.layout.addStretch()        
        
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
            
    def resize_table_to_content(self):
        total_height = self.table.horizontalHeader().height()
        for row in range(self.table.rowCount()):
            total_height += self.table.rowHeight(row)
        
        self.table.setFixedHeight(total_height)   
    
    def toggle_selected_players_table(self):
        if self.selected_players_table is None:
            self.create_selected_players_table()
        else:
            self.clear_selected_players_table()

    def create_selected_players_table(self):
        self.selected_players_table = QTableWidget()
        self.selected_players_table.setColumnCount(2)
        self.selected_players_table.setHorizontalHeaderLabels(["Player Name", "Select"])

        players = ["Player 1", "Player 2", "Player 3"]
        for player in players:
            row_position = self.selected_players_table.rowCount()
            player_item = QTableWidgetItem(player)
            checkbox_widget = CenteredCheckBoxWidget()
            self.selected_players_table.insertRow(row_position)
            self.selected_players_table.setItem(row_position, 0, player_item)
            self.selected_players_table.setCellWidget(row_position, 1, checkbox_widget)

        self.layout.insertWidget(self.layout.indexOf(self.manually_add_players_btn), self.selected_players_table)
        self.layout.insertWidget(self.layout.indexOf(self.selected_players_table) + 1, self.save_players_button)
        
        for row in range(self.selected_players_table.rowCount()):
            checkbox_widget = self.selected_players_table.cellWidget(row, 1)
            if isinstance(checkbox_widget, CenteredCheckBoxWidget):
                checkbox = checkbox_widget.layout().itemAt(0).widget()
                checkbox.stateChanged.connect(self.checkbox_state_changed)
    
    def clear_selected_players_table(self):
        self.layout.removeWidget(self.selected_players_table)
        self.selected_players_table.deleteLater()
        self.selected_players_table = None
        self.save_players_button.setVisible(False)
        
    def save_selected_players(self):
        selected_players = []
        for row in range(self.selected_players_table.rowCount()):
            checkbox_widget = self.selected_players_table.cellWidget(row, 1)
            if isinstance(checkbox_widget, CenteredCheckBoxWidget):
                if checkbox_widget.isChecked():
                    player_item = self.selected_players_table.item(row, 0)
                    selected_players.append(player_item.text())
        
        print("Selected Players:", selected_players)
        self.save_players_button.setVisible(False)
        
    def checkbox_state_changed(self, state):
        self.save_players_button.setVisible(True)