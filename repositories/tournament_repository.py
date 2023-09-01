from . import BaseRepository
from PySide6.QtCore import Qt, QDateTime
from models.tournament import Tournament
import json

class TournamentRepository(BaseRepository):
    TOURNAMENT_JSON_FILE_PATH = './data/tournaments/tournaments_data.json'
    
    def __init__(self, file_path = TOURNAMENT_JSON_FILE_PATH):
        super().__init__(file_path) 
            
    @staticmethod    
    def _serialize(tournament):
        return {
            "id": tournament.id,
            "name": tournament.name,
            "location": tournament.location,
            "start_date": tournament.start_date.toString(Qt.ISODate), 
            "end_date": tournament.end_date.toString(Qt.ISODate), 
            "num_rounds": int(tournament.num_rounds),
            "remarks": tournament.remarks
        }
        
    @staticmethod    
    def _deserialize(data):
        return Tournament(
            id=data["id"],
            name=data["name"],
            location=data["location"],
            start_date=QDateTime.fromString(data["start_date"], Qt.ISODate),
            end_date=QDateTime.fromString(data["end_date"], Qt.ISODate),
            num_rounds=data["num_rounds"],
            remarks=data["remarks"]
        )