from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QComboBox, QTreeWidget, QTreeWidgetItem, QHBoxLayout
from PySide6.QtCore import Qt, QDateTime
from models.tournament import Tournament
from models.match import MatchResult
from controllers.tournament_controller import TournamentController
from controllers.player_controller import PlayerController
from repositories.player_repository import PlayerRepository
from views.partials.date_delegate import DateDelegate
import random
# from views.partials.int_delegate import IntDelegate

class RoundReadView(QWidget):
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
        # self.previous_result = ""
        
        self.layout = QVBoxLayout()
        
        return_button = QPushButton('Go back to manager', self)
        return_button.clicked.connect(self.return_button_clicked)

        self.table = QTreeWidget(self)
        self.table.setHeaderLabel(f"{self.tournament.name}'s rounds list")

        self.layout.addWidget(return_button)
        self.layout.addWidget(self.table)

        # self.selected_players_table = None

        return_button.move(10, 10)
        self.setLayout(self.layout)
        
        # self.tournament_controller.save_new_item(self.tournament)
        self.tournament_controller.setup_view(self)
        
    def populate_table(self):  
        for round in self.tournament.rounds:
            tournament_item = QTreeWidgetItem(self.table, [round.name])

            for match in round.matches:
                string_color = "color" + str(random.randint(1,7))
                self.previous_result = match.result
                match_item = QTreeWidgetItem(tournament_item)
                nested_widget = QWidget()
                combo_widget = QWidget()
                nested_layout = QVBoxLayout(nested_widget)
                combo_layout = QHBoxLayout(combo_widget)
                combo_layout.setAlignment(Qt.AlignLeft)
                string_result = f"--> Result : * {match.get_winner()} *"
                combo_label = QLabel(string_result)
                combo_label.setObjectName("result")
                round_name = QLabel(match.get_match_name())
                round_name.setObjectName(string_color)
                
                # combo_box = QComboBox()
                # combo_box.addItem("Ex Aequo")
                # combo_box.setItemData(0, MatchResult.DRAW, Qt.UserRole)
                # combo_box.addItem(match.player1.get_full_name())
                # combo_box.setItemData(1, MatchResult.WIN, Qt.UserRole)
                # combo_box.addItem(match.player2.get_full_name())
                # combo_box.setItemData(2, MatchResult.LOSE, Qt.UserRole)
                # combo_box.setCurrentText(match.get_winner())
                # combo_box.currentIndexChanged.connect(lambda index, combo_box=combo_box, match=match: self.handle_combo_box_change(index, combo_box, match))                

                combo_layout.addWidget(combo_label)
                # combo_layout.addWidget(combo_box)
                nested_layout.addWidget(round_name)
                nested_layout.addWidget(combo_widget)
                self.table.setItemWidget(match_item, 0, nested_widget)

            tournament_item.setExpanded(True)
            
    def return_button_clicked(self):
        self.nav.switch_to_tournament_manager(self.tournament) 
            
    # def save_changes(self, combo_boxes_data, round, round_name=None, round_start_date=None, round_end_date=None):
    #     if combo_boxes_data:
    #         usable_data = []
    #         for combo_box_data in combo_boxes_data:
    #             combo_index = combo_box_data.currentIndex()
    #             usable_data.append(combo_box_data.itemData(combo_index, Qt.UserRole))
    #         self.tournament_controller.manage_round_data(round, usable_data, round_name, round_start_date, self.has_start_date_changed, round_end_date, self.has_end_date_changed)
    
    # def handle_combo_box_change(self, index, combo_box, current_match):
    #     try: 
    #         # matching_match = next((match for round in self.tournament.rounds if any(match == match for match in round.matches)), None)
    #         # round = next((round for round in self.tournament.rounds if any(match == current_match for match in round.matches)), None)
    #         selected_value = combo_box.itemData(index, Qt.UserRole)
    #         current_match.result = selected_value
    #         print(selected_value)
            
    #         print(self.previous_result)
            
    #         if selected_value == MatchResult.DRAW and self.previous_result == MatchResult.WIN :
    #             player_one_edited_score = current_match._draw_points - current_match._winning_points
    #             player_two_edited_score = current_match._draw_points - current_match._losing_points
    #             print(f"draw : {current_match._draw_points} + {current_match._winning_points} = {player_one_edited_score}")
    #             print(f"draw : {current_match._draw_points} + {current_match._losing_points} = {player_two_edited_score}")
                
    #         elif selected_value == MatchResult.DRAW and self.previous_result == MatchResult.LOSE : 
    #             player_one_edited_score = current_match._draw_points - current_match._losing_points
    #             player_two_edited_score = current_match._draw_points - current_match._winning_points
    #             print(f"draw : {current_match._draw_points} + {current_match._losing_points} = {player_one_edited_score}")
    #             print(f"draw : {current_match._draw_points} + {current_match._winning_points} = {player_two_edited_score}")
                
    #         elif selected_value == MatchResult.LOSE and self.previous_result == MatchResult.DRAW : 
    #             player_one_edited_score = current_match._losing_points - current_match._draw_points
    #             player_two_edited_score = current_match._winning_points - current_match._draw_points
    #             print(f"draw : {current_match._losing_points} + {current_match._draw_points} = {player_one_edited_score}")
    #             print(f"draw : {current_match._winning_points} + {current_match._draw_points} = {player_two_edited_score}")
                
    #         elif selected_value == MatchResult.LOSE and self.previous_result == MatchResult.WIN : 
    #             player_one_edited_score = current_match._losing_points - current_match._winning_points
    #             player_two_edited_score = current_match._winning_points - current_match._losing_points
    #             print(f"draw : {current_match._losing_points} + {current_match._winning_points} = {player_one_edited_score}")
    #             print(f"draw : {current_match._winning_points} + {current_match._losing_points} = {player_two_edited_score}")
                
    #         elif selected_value == MatchResult.WIN and self.previous_result == MatchResult.DRAW : 
    #             player_one_edited_score = current_match._winning_points - current_match._draw_points
    #             player_two_edited_score = current_match._losing_points - current_match._draw_points
    #             print(f"draw : {current_match._winning_points} + {current_match._draw_points} = {player_one_edited_score}")
    #             print(f"draw : {current_match._losing_points} + {current_match._draw_points} = {player_two_edited_score}")
                
    #         elif selected_value == MatchResult.WIN and self.previous_result == MatchResult.LOSE : 
    #             player_one_edited_score = current_match._winning_points - current_match._losing_points
    #             player_two_edited_score = current_match._losing_points - current_match._winning_points
    #             print(f"draw : {current_match._winning_points} + {current_match._losing_points} = {player_one_edited_score}")
    #             print(f"draw : {current_match._losing_points} + {current_match._winning_points} = {player_two_edited_score}")
                
    #         self.tournament_controller.save_changes(self.tournament)
    #         self.tournament_controller.modify_matches_results(current_match, player_one_edited_score, player_two_edited_score)
    #         self.previous_result = selected_value
    #     except Exception as e:
    #         print(f"Error fnding item: {e}")   
            
    def resize_table_to_content(self, table):
        total_height = table.horizontalHeader().height()
        for row in range(table.rowCount()):
            total_height += table.rowHeight(row)
        
        table.setFixedHeight(total_height)