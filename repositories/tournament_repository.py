from . import BaseRepository

class TournamentRepository(BaseRepository):
    TOURNAMENT_JSON_FILE_PATH = './data/tournaments/tournaments_data.json'
    
    def __init__(self, file_path = TOURNAMENT_JSON_FILE_PATH):
        super().__init__(file_path)

    def update_player(self, player):
        for existing_player in self.items:
            if existing_player.last_name == player.last_name and existing_player.first_name == player.first_name:
                existing_player.points = player.points
                break

    def add_round(self, round_data):
        self.add(round_data)