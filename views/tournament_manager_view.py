from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QDialog, QCheckBox, QComboBox, QHeaderView
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt, QDateTime, QTimer
from views.partials.input_field import InputField, FormType
from models.tournament import Tournament
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from repositories.player_repository import PlayerRepository
from views.partials.date_delegate import DateDelegate
from views.partials.int_delegate import IntDelegate
from views.partials.centered_check_box_widget import CenteredCheckBoxWidget
from views.player_read_view import PlayerReadView

class TournamentManagerView(QWidget):
    def __init__(self, nav, tournament, index=0):
        super().__init__()

        self._nav = nav
        self.tournament_controller = TournamentController(self._nav, tournament)
        self.player_controller = PlayerController(self._nav)
        self.tournament = tournament
        self.player_repository = PlayerRepository()
        self.date_delegate = DateDelegate(self)
        self.int_delegate = IntDelegate(self)
        self.all_players = self.player_repository.read_json()
        self.id_player_table_column = 3
        self.registered_players_column = 6
        self.id_main_table_column = 8
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
        
        self.table = None
        self.selected_players_table = None
        self.nbr_players_input = None
        self.cell_change_listener = True
        self.players_list = None
        
        self.view_player_button = QPushButton("See registered players")
        self.view_player_button.clicked.connect(self.see_players)
        self.layout.addWidget(self.view_player_button)
        self._check_view_player_button_visibility()
        
        self.manually_add_players_btn = QPushButton("Manually add players")
        self.manually_add_players_btn.clicked.connect(self.toggle_selected_players_table)
        self.layout.addWidget(self.manually_add_players_btn)               
        
        self.save_players_button = QPushButton("Save changes")
        self.save_players_button.clicked.connect(self.save_selected_players)
        self.save_players_button.setVisible(False)
        
        self.auto_add_players_btn = QPushButton("Automatically add players")
        self.auto_add_players_btn.clicked.connect(self.toggle_players_nbr_input)
        self.layout.addWidget(self.auto_add_players_btn)      
                
        self.auto_add_players_button_validation = QPushButton("Add players")
        self.auto_add_players_button_validation.clicked.connect(self.auto_select_players)
        self.auto_add_players_button_validation.setVisible(False)        
        
        self.start_simulation_btn = QPushButton("Simulate tournament")
        self.start_simulation_btn.clicked.connect(self.start_simulation)
        self.layout.addWidget(self.start_simulation_btn)
        
        self.toggle_buttons_visibility_check()       
        self.create_main_table()
        self.setLayout(self.layout)
        
        self.tournament_controller.setup_view(self)

    def populate_table(self):        
        id = QTableWidgetItem(self.tournament.id)
        id.setFlags(id.flags() & ~Qt.ItemIsEnabled)
        # self.table.setItemDelegateForColumn(2, self.date_delegate)
        # self.table.setItemDelegateForColumn(3, self.date_delegate)
        self.table.setItemDelegateForColumn(4, self.int_delegate)

        name = QTableWidgetItem(self.tournament.name)
        location = QTableWidgetItem(self.tournament.location)
        print("Data type tournamentmanager1.py:", type(self.tournament.start_date))

        start_date = QTableWidgetItem(self.tournament.start_date.toString(Qt.ISODate))
        start_date.setData(Qt.DisplayRole, start_date.text())
        start_date.setData(Qt.EditRole, self.tournament.start_date)
        print("Data type tournamentmanager2.py:", type(self.tournament.end_date))

        end_date = QTableWidgetItem(self.tournament.end_date.toString(Qt.ISODate))
        end_date.setData(Qt.DisplayRole, end_date.text())
        end_date.setData(Qt.EditRole, self.tournament.end_date)

        num_rounds = QTableWidgetItem(str(self.tournament._num_rounds))
        num_rounds.setData(Qt.EditRole, int(self.tournament._num_rounds))

        current_round = QTableWidgetItem(str(self.tournament._current_round))
        current_round.setFlags(current_round.flags() & ~Qt.ItemIsEnabled)
        
        registered_players = QTableWidgetItem(str(len(self.tournament._registered_players)))
        registered_players.setFlags(registered_players.flags() & ~Qt.ItemIsEnabled)

        remarks = QTableWidgetItem(self.tournament.remarks)
                
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, name)
        self.table.setItem(row_position, 1, location)
        self.table.setItem(row_position, 2, start_date)
        self.table.setItem(row_position, 3, end_date)
        self.table.setItem(row_position, 4, num_rounds)
        self.table.setItem(row_position, 5, current_round)
        self.table.setItem(row_position, self.registered_players_column, registered_players)
        self.table.setItem(row_position, 7, remarks)
        self.table.setItem(row_position, self.id_main_table_column, id)
        
        self.resize_table_to_content()
        self.table.itemChanged.connect(self.handle_item_changed)
        
        self.layout.addStretch()        
        
    def handle_item_changed(self, item):
        row = item.row()
        if self.cell_change_listener == True:
            try: 
                id_item = self.table.item(row, self.id_main_table_column) 
                tournament_id = id_item.text()            
                edited_tournament = self.tournament_controller.tournament_repository.find_one_by_id(tournament_id)
                edited_tournament.id=tournament_id
                edited_tournament.name=self.table.item(row, 0).text()
                edited_tournament.location=self.table.item(row, 1).text()
                edited_tournament.start_date=QDateTime.fromString(self.table.item(row, 2).text(), Qt.ISODate)
                edited_tournament.end_date=QDateTime.fromString(self.table.item(row, 3).text(), Qt.ISODate)
                edited_tournament.num_rounds=int(self.table.item(row, 4).text())
                edited_tournament.current_round=int(self.table.item(row, 5).text())
                edited_tournament.remarks=self.table.item(row, 7).text()
                    
                self.tournament_controller.save_changes(edited_tournament)
                self.toggle_buttons_visibility_check(edited_tournament)
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
            
    def toggle_players_nbr_input(self):
        if self.nbr_players_input is None:
            self.create_nbr_players_input()
        else:
            self.clear_nbr_players_input()

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
            self.selected_players_table.setCellWidget(row_position, self.id_player_table_column, checkbox_widget)

        self.layout.insertWidget(self.layout.indexOf(self.manually_add_players_btn) + 1, self.selected_players_table)
        self.layout.insertWidget(self.layout.indexOf(self.selected_players_table) + 1, self.save_players_button)
        # self.manually_add_players_btn.setVisible(False)
        
        for row in range(self.selected_players_table.rowCount()):
            checkbox_widget = self.selected_players_table.cellWidget(row, self.id_player_table_column)
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
        # self.manually_add_players_btn.setVisible(True)    
        
    def clear_main_table(self):
        self.layout.removeWidget(self.table)
        self.table.deleteLater()
        
    def actualize_main_table(self):
        self.clear_main_table()
        self.create_main_table()
        self.populate_table()

    def create_main_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Name", "Location", "Starting date", "Ending date", "Number of rounds", "Current round", "Players registered", "remarks"])
        self.table.setColumnHidden(self.id_main_table_column, True) 
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.layout.insertWidget(self.layout.indexOf(self.combo_box) + 1, self.table)
        
    def create_nbr_players_input(self):
        self.nbr_players_input = InputField(self.layout, "Number of players to implement", "Number of players", FormType.Numerical)
        self.nbr_players_input.displace(self.layout.indexOf(self.auto_add_players_btn) + 1)
        self.nbr_players_input.input.textChanged.connect(self.toggle_auto_add_btn_validation)
        self.layout.insertWidget(self.layout.indexOf(self.nbr_players_input.input) + 1, self.auto_add_players_button_validation)
        # self.auto_add_players_btn.setVisible(False)
        
    def toggle_auto_add_btn_validation(self, text):
        max_threshold = len(self.all_players)
        self.auto_add_players_button_validation.setVisible(True) if text else self.auto_add_players_button_validation.setVisible(False)
        if text and int(text) > max_threshold: self.nbr_players_input.set_text(max_threshold)
        
    def toggle_buttons_visibility_check(self,  tournament=""):
        if tournament == "": tournament = self.tournament
        self.toggle_start_simulation_button(tournament)
        self.toggle_add_player_button(tournament)
        
    def toggle_add_player_button(self, tournament):
        if int(tournament.current_round) > 1 and int(tournament.num_rounds) == len(tournament.rounds):
            self.auto_add_players_btn.setVisible(False)
            self.auto_add_players_button_validation.setVisible(False)
            self.save_players_button.setVisible(False)
            self.manually_add_players_btn.setVisible(False)        
        
    def toggle_start_simulation_button(self, tournament):
        self.start_simulation_btn.setVisible(True) if int(tournament.num_rounds) > len(tournament.rounds) and len(tournament.registered_players) > 0 and len(tournament.registered_players) % 2 == 0 else self.start_simulation_btn.setVisible(False)
        
    def auto_select_players(self):
        self.tournament_controller.clear_registered_players()
        try:
            registered_players_cell = self.find_cell(self.tournament.id, 6)
            if self.nbr_players_input : 
                selected_players = self.player_controller.randomly_pick_players(int(self.nbr_players_input.input.text()))
                for player in selected_players:
                    self.tournament_controller.add_player(player)
                    print(f"Successfully added player : {player.get_full_name()}")
            self.tournament_controller.save_changes(self.tournament)  
            #self.toggle_auto_add_btn_validation(None)                            
            self.toggle_players_nbr_input()                            
            self._check_view_player_button_visibility()      
            self.cell_change_listener = False
            if registered_players_cell is not None: registered_players_cell.setText(str(len(self.tournament.registered_players)))
            self.cell_change_listener = True     
            self.toggle_buttons_visibility_check()
        except Exception as e:
            print(f"Error adding players: {e}")

    def clear_nbr_players_input(self):        
        self.nbr_players_input.remove_widgets()
        self.auto_add_players_button_validation.setVisible(False)
        self.nbr_players_input = None
        # self.auto_add_players_btn.setVisible(True)
        
    def save_selected_players(self):
        self.tournament_controller.clear_registered_players()
        registered_players_cell = self.find_cell(self.tournament.id, 6)
        print(f"tournament : {self.tournament} tournament id : {self.tournament.id}")
        for row in range(self.selected_players_table.rowCount()):
            checkbox_widget = self.selected_players_table.cellWidget(row, self.id_player_table_column)
            if isinstance(checkbox_widget, CenteredCheckBoxWidget):
                if checkbox_widget.isChecked():
                    player_item = self.player_repository.find_one_by_id(self.selected_players_table.item(row, 0).text())
                    self.tournament_controller.add_player(player_item)
                    
        self.tournament_controller.save_changes(self.tournament)                    
        self.save_players_button.setVisible(False)
        self._check_view_player_button_visibility()           
        self.toggle_selected_players_table()
        self.cell_change_listener = False
        if registered_players_cell is not None: registered_players_cell.setText(str(len(self.tournament.registered_players)))
        self.cell_change_listener = True
        self.toggle_buttons_visibility_check()        
        # self.actualize_main_table()
        
    def checkbox_state_changed(self, state):
        self.save_players_button.setVisible(True)
        
    def start_simulation(self):
        self._nav.switch_to_tournament_simulator(self.tournament)
        
    def select_tournament(self):
        index = self.combo_box.currentIndex()
        selected_tournament = self.combo_box.itemData(index, role=Qt.UserRole)
        if selected_tournament:
            self._nav.switch_to_tournament_manager(selected_tournament, index)   
                
    def see_players(self):
        index = self.combo_box.currentIndex()
        selected_tournament = self.combo_box.itemData(index, role=Qt.UserRole)
        if selected_tournament and not self.players_list:
            print(f"len before: {len(self.tournament.registered_players)}")                        
            self.players_list = PlayerReadView(self._nav, self.tournament)
            self.players_list.closed.connect(self.on_players_list_closed)
            self.players_list.actualize_main_table()
            if int(self.tournament.current_round) > 1 and int(self.tournament.num_rounds) == len(self.tournament.rounds): self.players_list.hide_delete_column()
            self.players_list.show()
            # players_list.hide_delete_column()
            
    def _check_view_player_button_visibility(self):
        self.view_player_button.setVisible(True) if self.tournament and len(self.tournament.registered_players) > 0 else self.view_player_button.setVisible(False)            
        
    def find_cell(self, value, col):

        for row in range(self.table.rowCount()):
            item = self.table.item(row, self.id_main_table_column)
            if item and item.text() == value:
                print(f"row : {row}, current cell value : {self.table.item(row, self.id_main_table_column).text()}")
                return self.table.item(row, col)

        print(f"Value '{value}' not found.")
        
    def on_players_list_closed(self):
        QTimer.singleShot(100, self.destroy_players_list)
        
    def destroy_players_list(self):
        self.sender().deleteLater()
        registered_players_cell = self.find_cell(self.tournament.id, 6)
        if not self.paintingActive(): 
            self.cell_change_listener = False
            if registered_players_cell is not None: registered_players_cell.setText(str(len(self.tournament.registered_players)))
            self.cell_change_listener = True
            self.players_list = None
            self.toggle_buttons_visibility_check()   
            self._check_view_player_button_visibility()    
            
