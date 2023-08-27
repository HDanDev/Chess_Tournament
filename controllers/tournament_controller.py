from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from PySide6.QtCore import QDateTime 
from repositories.tournament_repository import TournamentRepository
from models.match import MatchResult, Match
from models.round import Round
from models.tournament import Tournament
import random 
from datetime import datetime

class TournamentController:
    
    def __init__(self, nav, tournament={}):
        self.nav = nav
        self.tournament = tournament
        self.tournament_repository = TournamentRepository()
        self.tournament_model = Tournament
        
    def setup_view(self, view):
        self.view = view
        self.view.populate_table()
        self.view.table.horizontalHeader().setStretchLastSection(True)
        self.view.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
    def get_tournament_data(self):
        return self.tournament_repository._read_json()

    def save_changes(self, tournament):
        self.tournament_repository._update_json(tournament)
        
    def save_new_item(self, tournament):
        self.tournament_repository._add_json(tournament)
        
    def add_player(self, player):
        try:
            self.tournament.registered_players.append(player)
        except Exception as e:
            print(f"Error adding player: {e}")
            
    def generate_pairs(self):
        try:
            new_round = Round()
            new_round.name = f"Round {self.tournament.current_round}"
            new_round.start_datetime = datetime.now()
            new_round.end_datetime = None            
            
            if self.tournament.current_round == 1:
                random.shuffle(self.tournament.registered_players)
                sorted_players = self.tournament.registered_players
                
            else: 
                sorted_players = sorted(self.tournament.registered_players, key=lambda p: p.points, reverse=True)

            for i in range(0, len(sorted_players), 2):
                if i + 1 < len(sorted_players):
                    new_match = Match()
                    new_match.player1 = sorted_players[i]
                    new_match.player2 = sorted_players[i + 1]                    
                    new_round.add_match(new_match)    

            self.tournament.add_round(new_round)

            self.tournament.current_round += 1
            
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
            
    def check_is_player_already_selected(self, tournament_players, all_players, id):
        tournament_players_ids = set(player.chess_id for player in tournament_players)
        all_players_ids = set(player.chess_id for player in all_players)

        return id in tournament_players_ids and id in all_players_ids

    
