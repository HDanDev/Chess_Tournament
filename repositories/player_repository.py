from . import BaseRepository

class PlayerRepository(BaseRepository):
    PLAYERS_JSON_FILE_PATH = './data/players/players_data.json'
    
    def __init__(self, PLAYERS_JSON_FILE_PATH):
        super().__init__(PLAYERS_JSON_FILE_PATH)
        
    def add(self, player):
        self.data.append({
            "last_name": player.last_name,
            "first_name": player.first_name,
            "points": player.points
        })
        self.save_data()

    def update(self, player):
        for existing_player in self.data:
            if (existing_player["last_name"] == player.last_name and
                    existing_player["first_name"] == player.first_name):
                existing_player["points"] = player.points
                self.save_data()
                break
            
    def get_assigned_ids(self):
        data = self._read_data_from_file()
        return [item['id'] for item in data]
        