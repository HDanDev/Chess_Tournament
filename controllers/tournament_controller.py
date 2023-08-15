from . import BaseController
from views.tournament_create_view import TournamentCreateView
from models.match import MatchResult
import random 
from datetime import datetime

class TournamentController(BaseController):
    def __init__(self):
        super().__init__(TournamentCreateView)      

    def _handle_button_click(self, button_text):
        if button_text == "Create":
            self._handle_create_button()
        elif button_text == "Create2":
            self._handle_create2_button()
        elif button_text == "Read":
            self._handle_read_button()
        elif button_text == "Exit":
            self.view.close()

    def _handle_create_button(self):
        self._get_input_data()

    def _handle_create2_button(self):
        print("Create2 button clicked")

    def _handle_read_button(self):
        print("Read button clicked")
        
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
