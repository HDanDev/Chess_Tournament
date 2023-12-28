from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QComboBox
from PySide6.QtCore import Qt, QDateTime
from views.partials.input_field import InputField, FormType
from models.tournament import Tournament
from models.match import MatchResult
from controllers.tournament_controller import TournamentController
from repositories.player_repository import PlayerRepository
from views.partials.date_delegate import DateDelegate
# from views.partials.int_delegate import IntDelegate

class RoundManager(QWidget):
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
        self.has_start_date_changed = False
        self.has_end_date_changed = False
        
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
        round_nbr = len(self.tournament.rounds) + 1
        print(f"self.tournament.num_rounds : {self.tournament.num_rounds}")
        print(f"i : {round_nbr}")
        print(f"currentround : {self.tournament.current_round}")
        print(f"length : {len(self.tournament.rounds)}")        
        self.tournament_controller.generate_pairs(current_round=round_nbr) 
        self.create_round_table(self.tournament.rounds[round_nbr - 1])

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
        
        self.save_btn = QPushButton("Save and go next round")
        self.save_btn.clicked.connect(lambda: self.next_round(combo_boxes_data, round, round_name.input.text(), start_date.input.dateTime(), end_date.input.dateTime()))
        
        self.next_auto = QPushButton("Save and simulate next round")
        self.next_auto.clicked.connect(lambda: self.simulate_next(combo_boxes_data, round, round_name.input.text(), start_date.input.dateTime(), end_date.input.dateTime()))
        
        self.all_auto = QPushButton("Save and simulate whole tournament")
        self.all_auto.clicked.connect(lambda: self.simulate_all(combo_boxes_data, round, round_name.input.text(), start_date.input.dateTime(), end_date.input.dateTime()))
                
        round_name = InputField(self.layout, "Round name", "Round name")
        
        start_date = InputField(self.layout, "Round start date", "Round start date", FormType.DateTime)
        start_date.input.dateTimeChanged.connect(self.toggle_start_date)
        
        end_date = InputField(self.layout, "Round end date", "Round end date", FormType.DateTime)
        end_date.input.dateTimeChanged.connect(self.toggle_end_date)
        
        self.layout.addWidget(round_table)
        self.layout.addWidget(self.save_btn)
        self.layout.addWidget(self.next_auto)
        self.layout.addWidget(self.all_auto) 
        
    def save_changes(self, combo_boxes_data, round, round_name=None, round_start_date=None, round_end_date=None):
        if combo_boxes_data:
            usable_data = []
            for combo_box_data in combo_boxes_data:
                combo_index = combo_box_data.currentIndex()
                usable_data.append(combo_box_data.itemData(combo_index, Qt.UserRole))
            self.tournament_controller.manage_round_data(round, usable_data, round_name, round_start_date, self.has_start_date_changed, round_end_date, self.has_end_date_changed)
        
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
        
    def toggle_start_date(self):
        self.has_start_date_changed = True
        
    def toggle_end_date(self):
        self.has_end_date_changed = True
        
    def next_round(self, combo_boxes_data, round, round_name=None, round_start_date=None, round_end_date=None):
        self.save_changes(combo_boxes_data, round, round_name, round_start_date, round_end_date)
        if int(self.tournament.current_round) < int(self.tournament.num_rounds):
            self.nav.switch_to_round_manager(self.tournament) 
        else: 
            print("Tournament is over")
            self.save_btn.setVisible(False)           
            
    def simulate_next(self, combo_boxes_data, round, round_name=None, round_start_date=None, round_end_date=None):
        self.save_changes(combo_boxes_data, round, round_name, round_start_date, round_end_date)
        if int(self.tournament.current_round) < int(self.tournament.num_rounds):
            self.nav.switch_to_tournament_step_by_step_simulator(self.tournament) 
        else: 
            print("Tournament is over")
            self.next_auto.setVisible(False)
            
    def simulate_all(self, combo_boxes_data, round, round_name=None, round_start_date=None, round_end_date=None):
        self.save_changes(combo_boxes_data, round, round_name, round_start_date, round_end_date)
        if int(self.tournament.current_round) < int(self.tournament.num_rounds):
            self.nav.switch_to_tournament_simulator(self.tournament) 
        else: 
            print("Tournament is over")
            self.all_auto.setVisible(False)
        