from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QDialog, QCheckBox, QComboBox
from PySide6.QtCore import Qt, QDateTime
from views.partials.input_field import InputField, FormType
from models.tournament import Tournament
from controllers.tournament_controller import TournamentController
from repositories.player_repository import PlayerRepository
from views.partials.date_delegate import DateDelegate
from views.partials.int_delegate import IntDelegate
from views.partials.centered_check_box_widget import CenteredCheckBoxWidget

class TournamentManagerView(QWidget):
    def __init__(self, nav, tournament, index=0):
        super().__init__()

        self._nav = nav
        self.tournament_controller = TournamentController(self._nav, tournament)
        self.tournament = tournament
        self.player_repository = PlayerRepository()
        self.date_delegate = DateDelegate(self)
        self.int_delegate = IntDelegate(self)
        self.all_players = self.player_repository.read_json()
        self.id_index_column = 3
        self.combo_index = index
        
        self.layout = QVBoxLayout()

        self.label = QLabel("Tournament Manager")
        self.layout.addWidget(self.label)
        
        self.combo_box = QComboBox()

        for tournament in self.tournament_controller.get_tournament_data():
            item = tournament.name
            self.combo_box.addItem(item)
            self.combo_box.setItemData(self.combo_box.count() - 1, tournament, role=Qt.UserRole)
            
        self.combo_box.setCurrentIndex(self.combo_index)

        self.layout.addWidget(self.combo_box)
        self.combo_box.currentIndexChanged.connect(self.select_tournament)

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
        
        self.start_simulation_btn = QPushButton("Simulate tournament")
        self.start_simulation_btn.clicked.connect(self.start_simulation)
        self.layout.addWidget(self.start_simulation_btn)
        
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
        self.selected_players_table.setColumnCount(4)
        self.selected_players_table.setHorizontalHeaderLabels(["Player chess ID", "Player first name", "Player last name", "Select"])

        for player in self.all_players:
            row_position = self.selected_players_table.rowCount()
            
            player_chess_id = QTableWidgetItem(player.chess_id)
            player_chess_id.setFlags(player_chess_id.flags() & ~Qt.ItemIsEnabled)
            
            player_first_name = QTableWidgetItem(player.first_name)
            player_first_name.setFlags(player_first_name.flags() & ~Qt.ItemIsEnabled)
            
            player_last_name = QTableWidgetItem(player.last_name)
            player_last_name.setFlags(player_last_name.flags() & ~Qt.ItemIsEnabled)
            
            checkbox_widget = CenteredCheckBoxWidget()
            self.selected_players_table.insertRow(row_position)
            self.selected_players_table.setItem(row_position, 0, player_chess_id)
            self.selected_players_table.setItem(row_position, 1, player_first_name)
            self.selected_players_table.setItem(row_position, 2, player_last_name)
            self.selected_players_table.setCellWidget(row_position, self.id_index_column, checkbox_widget)

        self.layout.insertWidget(self.layout.indexOf(self.manually_add_players_btn), self.selected_players_table)
        self.layout.insertWidget(self.layout.indexOf(self.selected_players_table) + 1, self.save_players_button)
        
        for row in range(self.selected_players_table.rowCount()):
            checkbox_widget = self.selected_players_table.cellWidget(row, self.id_index_column)
            if isinstance(checkbox_widget, CenteredCheckBoxWidget):
                checkbox = checkbox_widget.layout().itemAt(0).widget()
                if self.tournament_controller.check_is_player_already_selected(self.tournament.registered_players, self.all_players, self.selected_players_table.item(row, 0).text()):
                    checkbox_widget.setChecked(True)
                checkbox.stateChanged.connect(self.checkbox_state_changed)
    
    def clear_selected_players_table(self):
        self.layout.removeWidget(self.selected_players_table)
        self.selected_players_table.deleteLater()
        self.selected_players_table = None
        self.save_players_button.setVisible(False)
        
    def save_selected_players(self):
        self.tournament.registered_players = []
        for row in range(self.selected_players_table.rowCount()):
            checkbox_widget = self.selected_players_table.cellWidget(row, self.id_index_column)
            if isinstance(checkbox_widget, CenteredCheckBoxWidget):
                if checkbox_widget.isChecked():
                    player_item = self.player_repository.find_one_by_id(self.selected_players_table.item(row, 0).text())
                    self.tournament_controller.add_player(player_item)
                    
        self.save_players_button.setVisible(False)
        self.toggle_selected_players_table()
        
    def checkbox_state_changed(self, state):
        self.save_players_button.setVisible(True)
        
    def start_simulation(self):
        self._nav.switch_to_tournament_simulator(self.tournament)
        
    def select_tournament(self):
        index = self.combo_box.currentIndex()
        selected_tournament = self.combo_box.itemData(index, role=Qt.UserRole)
        if selected_tournament:
            self._nav.switch_to_tournament_manager(selected_tournament, index)
        
        
        