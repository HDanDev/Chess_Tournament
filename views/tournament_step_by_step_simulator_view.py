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

class TournamentStepByStepSimulatorView(QWidget):
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
        self.tournament_controller.generate_pairs(current_round=round_nbr, is_simulation=True) 
        self.create_round_table(self.tournament.rounds[round_nbr - 1])

    def create_round_table(self, round):
        title = QLabel(f"Round \"{round.name}\" ended at {round.end_datetime.toString('dddd, yyyy-MM-dd HH:mm:ss')}")
        round_table = QTableWidget()
        round_table.setColumnCount(2)
        round_table.setHorizontalHeaderLabels(["Matches", "Winner"])
    
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
            
        self.next_manual = QPushButton("Manage next round")
        self.next_manual.clicked.connect(self.next_round)
        
        self.next_auto = QPushButton("Simulate next round")
        self.next_auto.clicked.connect(self.simulate_next)
        
        self.all_auto = QPushButton("Simulate whole tournament")
        self.all_auto.clicked.connect(self.simulate_all)
        
        self.layout.addWidget(round_table)
        self.layout.addWidget(self.next_manual)
        self.layout.addWidget(self.next_auto)
        self.layout.addWidget(self.all_auto) 
            
    def resize_table_to_content(self, table):
        total_height = table.horizontalHeader().height()
        for row in range(table.rowCount()):
            total_height += table.rowHeight(row)
        
        table.setFixedHeight(total_height)
        
    def next_round(self):
        if int(self.tournament.current_round) < int(self.tournament.num_rounds):
            self.nav.switch_to_round_manager(self.tournament) 
        else: 
            print("Tournament is over")
            self.next_manual.setVisible(False)
            
    def simulate_next(self):
        if int(self.tournament.current_round) < int(self.tournament.num_rounds):
            self.nav.switch_to_tournament_step_by_step_simulator(self.tournament) 
        else: 
            print("Tournament is over")
            self.next_auto.setVisible(False)
            
    def simulate_all(self):
        if int(self.tournament.current_round) < int(self.tournament.num_rounds):
            self.nav.switch_to_tournament_simulator(self.tournament) 
        else: 
            print("Tournament is over")
            self.all_auto.setVisible(False)