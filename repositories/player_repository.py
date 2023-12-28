from . import BaseRepository
from PySide6.QtCore import Qt, QDate
from models.player import Player
import json, os

class PlayerRepository(BaseRepository):
    PLAYER_JSON_FILE_PATH = './data/players/players_data.json'
    
    def __init__(self, file_path = PLAYER_JSON_FILE_PATH):
        super().__init__(file_path)
        self._attribute = "chess_id"       
            
    def add_json(self, player):
        serialized_player = None

        if self.__is_id_assigned(player.chess_id, self.__get_assigned_ids()):
            raise ValueError(f"ID: {player.chess_id} is already in use, the chess ID has to be unique. Maybe the player has already been registered.")
        
        serialized_player = self.serialize_player(player)
        data = []

        try:
            with open(self._file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            pass

        if serialized_player:
            data.append(serialized_player)
    
        temp_file_path = self._file_path + ".temp"
        is_success = False

        try:
            with open(temp_file_path, "w") as file:
                json.dump(data, file, indent=4)
                is_success = True
                
        except Exception as e:
            print(f"An error occurred: {str(e)}, therefore the json file has not been updated")
            
        if is_success : os.replace(temp_file_path, self._file_path)
            
    def __is_id_assigned(self, new_id, assigned_ids):
        return new_id in assigned_ids
        
    def __get_assigned_ids(self):
        data = self.read_json()
        return [item.chess_id for item in data]          
    
    @staticmethod    
    def _serialize(player):
        return {
            "first_name": player.first_name,
            "last_name": player.last_name,
            "date_of_birth": player.date_of_birth.toString(Qt.ISODate), 
            "chess_id": player.chess_id,
            "tournament_score": player.points
        }
        
    @staticmethod    
    def _deserialize(data):
        player = Player()
        
        player.first_name = data["first_name"]
        player.last_name = data["last_name"]
        player.date_of_birth = QDate.fromString(data["date_of_birth"], Qt.ISODate)
        player.chess_id = data["chess_id"]    
        player.points = data.get("tournament_score", {})     
            
        return player