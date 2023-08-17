from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from repositories.tournament_repository import TournamentRepository
from models.match import MatchResult
import random 
from datetime import datetime

class TournamentController:
    
    def __init__(self, main_app, user_data={}):
        self.main_app = main_app
        self.user_data = user_data
        self.data_repository = TournamentRepository()
        
    def setup_view(self, view):
        self.view = view
        self.view.populate_table(self.user_data)
        self.view.table.horizontalHeader().setStretchLastSection(True)
        self.view.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def save_changes(self):
        for row in range(self.view.table.rowCount()):
            username_item = self.view.table.item(row, 0)
            password_item = self.view.table.item(row, 1)
            if username_item and password_item:
                username = username_item.text()
                password = password_item.text()
                self.user_data[row]["username"] = username
                self.user_data[row]["password"] = password

        self.data_repository._write_data_to_file(self.user_data)
        
    def add_player(self, player):
        try:
            self.registered_players.append(player)
        except Exception as e:
            print(f"Error adding player: {e}")
            
    def generate_pairs(self):
        try:
            if self.current_round == 1:
                random.shuffle(self.players)

            sorted_players = sorted(self.players, key=lambda p: p.points, reverse=True)
            pairs = []

            for i in range(0, len(sorted_players), 2):
                if i + 1 < len(sorted_players):
                    pairs.append((sorted_players[i], sorted_players[i + 1]))

            self.rounds.append({
                "name": f"Round {self.current_round}",
                "start_time": datetime.now(),
                "end_time": None,
                "matches": pairs
            })

            self.current_round += 1
        except Exception as e:
            print(f"Error generating pairs: {e}")         
            
    def play_match(self, match):
        try:
            if match.result == MatchResult.WIN:
                match.player1.points += 1
            elif match.result == MatchResult.LOSE:
                match.player2.points += 1
            elif match.result == MatchResult.DRAW:
                match.player1.points += 0.5
                match.player2.points += 0.5
        except Exception as e:
            print(f"Error playing match: {e}")
