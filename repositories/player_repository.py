from . import BaseRepository
from PySide6.QtCore import Qt, QDateTime
from models.player import Player
import json

class IDAlreadyAssignedError(Exception):
    pass

class PlayerRepository(BaseRepository):
    PLAYER_JSON_FILE_PATH = './data/players/players_data.json'
    
    def __init__(self, file_path = PLAYER_JSON_FILE_PATH):
        super().__init__(file_path)
        
    def _read_json(self):
        players = []
        try:
            with open(self.file_path, 'r') as file:
                deserialized_players = json.load(file)
                for data in deserialized_players:
                    players.append(self.deserialize_player(data))
        except FileNotFoundError as e:
            print(f"Could not find the file: {e}")
        return players

        
    def _write_json(self, players):
        try:
            serialized_players = [self.serialize_player(player) for player in players]
            with open(self.file_path, 'w') as file:
                json.dump(serialized_players, file, indent=4)
        except FileNotFoundError as e:
            print(f"Could not find the file: {e}")

    def _update_json(self, player):
        try:
            data = self._read_json()

            for i, item in enumerate(data):
                if item.id == player.id:
                    data[i] = player
                    break

            with open(self.file_path, 'w') as file:
                serialized_data = [self.serialize_player(item) for item in data]
                json.dump(serialized_data, file, indent=4)
        except FileNotFoundError:
            print(f"Could not find the file: {self.file_path}")
            
    def _add_json(self, player):
        serialized_player = None

        if self.is_id_assigned(player.chess_id, self.get_assigned_ids()):
            raise ValueError(f"ID: {player.chess_id} is already in use, the chess ID has to be unique. Maybe the player has already been registered.")
        
        serialized_player = self.serialize_player(player)
        data = []
        print(serialized_player)

        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            pass

        if serialized_player:
            data.append(serialized_player)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
            
    def is_id_assigned(self, new_id, assigned_ids):
        return new_id in assigned_ids
        
    def get_assigned_ids(self):
        data = self._read_json()
        return [item.chess_id for item in data]          
    
    def serialize_player(self, player):
       
        return {
            "first_name": player.first_name,
            "last_name": player.last_name,
            "date_of_birth": player.date_of_birth.toString(Qt.ISODate), 
            "chess_id": player.chess_id
        }
        
    @staticmethod    
    def deserialize_player(data):
        player = Player()
        
        player.first_name = data["first_name"]
        player.last_name = data["last_name"]
        player.date_of_birth = QDateTime.fromString(data["date_of_birth"], Qt.ISODate)
        player.chess_id = data["chess_id"]        

        return player