from . import BaseRepository
from PySide6.QtCore import Qt, QDateTime
from models.tournament import Tournament
import json

class TournamentRepository(BaseRepository):
    TOURNAMENT_JSON_FILE_PATH = './data/tournaments/tournaments_data.json'
    
    def __init__(self, file_path = TOURNAMENT_JSON_FILE_PATH):
        super().__init__(file_path) 
            
    def _serialize(self, tournament):
        registered_players = []        
        for player in tournament.registered_players:
            registered_players.append(self.serialize_player(player))
            
        return {
            "id": tournament.id,
            "name": tournament.name,
            "location": tournament.location,
            "start_date": tournament.start_date.toString(Qt.ISODate), 
            "end_date": tournament.end_date.toString(Qt.ISODate), 
            "num_rounds": int(tournament.num_rounds),
            "remarks": tournament.remarks,            
            "registered_players": registered_players
        }
        
    def _deserialize(self, data):
        tournament =  Tournament(
            id=data["id"],
            name=data["name"],
            location=data["location"],
            start_date=QDateTime.fromString(data["start_date"], Qt.ISODate),
            end_date=QDateTime.fromString(data["end_date"], Qt.ISODate),
            num_rounds=data["num_rounds"],
            remarks=data["remarks"]
        )         
        registered_players = []    
        for player in data["registered_players"]:
            registered_players.append(self.deserialize_player(player))
        tournament.registered_players = registered_players
        
        return tournament