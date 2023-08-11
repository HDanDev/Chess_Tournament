from . import BaseRepository

class PlayerRepository(BaseRepository):
    def __init__(self, file_path):
        super().__init__(file_path)
        
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