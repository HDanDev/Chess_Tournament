from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QDialog, QCheckBox, QComboBox, QHBoxLayout, QDateEdit, QHeaderView
from PySide6.QtCore import Qt, QDateTime
from views.partials.input_field import InputField, FormType
from models.tournament import Tournament
from models.match import MatchResult
from controllers.tournament_controller import TournamentController
from repositories.player_repository import PlayerRepository
from views.partials.date_delegate import DateDelegate
from views.partials.int_delegate import IntDelegate
from views.partials.centered_check_box_widget import CenteredCheckBoxWidget

class TournamentSimulatorView(QWidget):
    def __init__(self, nav, tournament):
        super().__init__()

        self.nav = nav
        self.tournament_controller = TournamentController(nav, tournament)
        self.tournament = tournament
        self.player_repository = PlayerRepository()
        self.date_delegate = DateDelegate(self)
        self.int_delegate = IntDelegate(self)
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
        if len(self.tournament.rounds) == 0:  
            if int(self.tournament.num_rounds) > 1:   
                print("case1")
                for i in range(1, int(self.tournament.num_rounds)):
                    self.tournament_controller.generate_pairs(current_round=int(i)) 
                    self.create_round_table(self.tournament.rounds[int(i)-1])
                    print(f"self.tournament.num_rounds : {self.tournament.num_rounds}")
                    print(f"i : {i}")
                    print(f"currentround : {self.tournament.current_round}")
                    print(f"length : {len(self.tournament.rounds)}")
                    
            else:  
                print("case2")
                self.tournament_controller.generate_pairs() 
                self.create_round_table(self.tournament.rounds[0]) 
                print(f"self.tournament.num_rounds : {self.tournament.num_rounds}")
                print(f"currentround : {self.tournament.current_round}")
                print(f"length : {len(self.tournament.rounds)}")
        else:
            if int(self.tournament.num_rounds) > 1 and self.tournament.num_rounds is not len(self.tournament.rounds) :   
                print("case3")
                for round in self.tournament.rounds:
                    self.create_immutable_round_table(round)
                    print(f"self.tournament.num_rounds : {self.tournament.num_rounds}")
                    print(f"currentround : {self.tournament.current_round}")
                    print(f"length : {len(self.tournament.rounds)}")
                for i in range(len(self.tournament.rounds), self.tournament.num_rounds):
                    self.tournament_controller.generate_pairs(current_round=int(i+1)) 
                    self.create_round_table(self.tournament.rounds[i])
                    print(f"self.tournament.num_rounds : {self.tournament.num_rounds}")
                    print(f"i : {i}")
                    print(f"currentround : {self.tournament.current_round}")
                    print(f"length : {len(self.tournament.rounds)}")
            else:
                print("case4")
                for round in self.tournament.rounds:
                    self.create_immutable_round_table(round)
                    print(f"self.tournament.num_rounds : {self.tournament.num_rounds}")
                    print(f"currentround : {self.tournament.current_round}")
                    print(f"length : {len(self.tournament.rounds)}")
            

    def create_round_table(self, round):
        round_table = QTableWidget()
        round_table.setColumnCount(2)
        round_table.setHorizontalHeaderLabels(["Matches", "Winner"])
        
        if round.matches and len(round.matches) > 0:
            combo_boxes_data = []

            for match in round.matches :            
                row_position = round_table.rowCount()
                round_table.insertRow(row_position)

                matches_item = QTableWidgetItem(f"{match.player1.get_full_name()} vs {match.player2.get_full_name()}")
                matches_item.setFlags(matches_item.flags() & ~Qt.ItemIsEditable)
                round_table.setItem(row_position, 0, matches_item)
                
                combo_box = QComboBox()
                combo_box.addItem("Ex Aequo")
                combo_box.setItemData(0, MatchResult.DRAW, Qt.UserRole)
                combo_box.addItem(match.player1.get_full_name())
                combo_box.setItemData(1, MatchResult.WIN, Qt.UserRole)
                combo_box.addItem(match.player2.get_full_name())
                combo_box.setItemData(2, MatchResult.LOSE, Qt.UserRole)
                combo_box.setCurrentText("Ex Aequo")
                round_table.setCellWidget(row_position, 1, combo_box)
                
                combo_boxes_data.append(combo_box)
            
        self.resize_table_to_content(round_table)
        
        end_date = InputField(self.layout, "Round end date", "Round en date", FormType.DateTime)
        self.tournament_controller.set_round_end_date(round, end_date.input.dateTime())
        print(f"{round.name} end at {round.end_datetime}")
        
        self.simulation_button = QPushButton("Get info")
        self.simulation_button.clicked.connect(lambda: self.get_combo_boxes_data(combo_boxes_data))
        
        self.layout.addWidget(round_table)
        self.layout.addWidget(self.simulation_button)
        
        
    def create_immutable_round_table(self, round):
        print("Data type tournament simulator.py:", type(round.end_datetime))
        title = QLabel(f"Round \"{round.name}\" ended at {round.end_datetime.toString('dddd, yyyy-MM-dd HH:mm:ss')}")
        round_table = QTableWidget()
        round_table.setColumnCount(2)
        round_table.setHorizontalHeaderLabels(["Matches", "Winner"])
        
        if round.matches and len(round.matches) > 0:

            for match in round.matches :            
                row_position = round_table.rowCount()
                round_table.insertRow(row_position)

                matches_item = QTableWidgetItem(f"{match.player1.get_full_name()} vs {match.player2.get_full_name()}")
                matches_item.setFlags(matches_item.flags() & ~Qt.ItemIsEditable)
                round_table.setItem(row_position, 0, matches_item)
                
                result = QTableWidgetItem(f"{match.get_winner()}")
                result.setFlags(result.flags() & ~Qt.ItemIsEditable)
                round_table.setItem(row_position, 1, result)
            
        self.resize_table_to_content(round_table)
        
        self.layout.addWidget(title)
        self.layout.addWidget(round_table)
        
    def get_combo_boxes_data(self, combo_boxes_data):
        if combo_boxes_data:
            usable_data = []
            for combo_box_data in combo_boxes_data:
                combo_index = combo_box_data.currentIndex()
                usable_data.append(combo_box_data.itemData(combo_index, Qt.UserRole))
            self.tournament_controller.update_matches_results(usable_data)
        
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
            
    def resize_table_to_content(self, table):
        total_height = table.horizontalHeader().height()
        for row in range(table.rowCount()):
            total_height += table.rowHeight(row)
        
        table.setFixedHeight(total_height)   
    
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
                    self.tournament.registered_players.append(player_item)
                    
        self.save_players_button.setVisible(False)
        
    def checkbox_state_changed(self, state):
        self.save_players_button.setVisible(True)