from PySide6.QtWidgets import QTableWidgetItem, QHeaderView
from PySide6.QtCore import QDateTime, Qt
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
        return self.tournament_repository.read_json()

    def save_changes(self, tournament):
        self.tournament_repository.update_json(tournament)
        
    def save_new_item(self, tournament):
        self.tournament_repository.add_json(tournament)        
        
    def delete_one(self, id):
        self.tournament_repository.delete_json(id)
        
    def add_player(self, player):
        try:
            self.tournament.add_player(player)
        except Exception as e:
            print(f"Error adding player: {e}")
            
    def remove_player(self, player):
        try:
            self.tournament.remove_player(player)
        except Exception as e:
            print(f"Error removing player: {e}")
            
            
    def clear_registered_players(self):
        self.tournament.registered_players.clear()
            
    def generate_pairs(self, is_simulation = False, current_round=1):
        try:
            self.tournament.current_round = current_round
            
            new_round = Round()
            new_round.name = f"Round {self.tournament.current_round}"
            new_round.start_datetime = QDateTime.currentDateTime()
            new_round.end_datetime = QDateTime.currentDateTime()           
            
            if self.tournament.current_round == 1:
                random.shuffle(self.tournament.registered_players)
                sorted_players = self.tournament.registered_players
                
            else: 
                sorted_players = sorted(self.tournament.registered_players, key=lambda p: p.points, reverse=True)
                # sorted_players = sorted(self.tournament.registered_players, key=lambda player: player[1], reverse=True)                

            for i in range(0, len(sorted_players), 2):
                if i + 1 < len(sorted_players):
                    new_match = Match()
                    new_match.player1 = sorted_players[i]
                    new_match.player2 = sorted_players[i + 1]                    
                    new_round.add_match(new_match)    
            print(f"this tournament currently count {len(self.tournament.rounds)}")
            self.tournament.add_round(new_round)
            checker = 0
            print(f"just added a round: {self.tournament.rounds[checker]}")
            checker = checker+1
            
            
            is_simulation = True
            if is_simulation:
                outcome = list(MatchResult)
                
                for match in new_round.matches:
                    random_result = random.choice(outcome)
                    match.result = random_result
                    print(f"Outcome of {match.get_match_name()}: {match.result} / player one has now: {match.get_match_result()[0][1]} points, and player 2: {match.get_match_result()[1][1]} points")
            
            self.save_changes(self.tournament)
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
    
    def set_round_end_date(self, round, date):
        
        print("Data type tournament_controller:", type(date))
        round.end_datetime = date

    
