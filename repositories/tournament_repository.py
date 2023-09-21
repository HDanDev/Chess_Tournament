from . import BaseRepository
from PySide6.QtCore import Qt, QDateTime
from models.tournament import Tournament
from models.round import Round
import json

class TournamentRepository(BaseRepository):
    TOURNAMENT_JSON_FILE_PATH = './data/tournaments/tournaments_data.json'
    
    def __init__(self, file_path = TOURNAMENT_JSON_FILE_PATH):
        super().__init__(file_path) 
        self._round_model = Round()
            
    def _serialize(self, tournament):
        try:
            registered_players = []        
            for player in tournament.registered_players:
                registered_players.append(self.serialize_player(player))           
                
            rounds = []
            if tournament.rounds and len(tournament.rounds) > 0:
                for round in tournament.rounds:
                    rounds.append(round.serialize())
            return {
                "id": tournament.id,
                "name": tournament.name,
                "location": tournament.location,
                "start_date": tournament.start_date.toString(Qt.ISODate), 
                "end_date": tournament.end_date.toString(Qt.ISODate), 
                "num_rounds": int(tournament.num_rounds),
                "current_round": int(tournament.current_round),
                "total_registered_players": int(tournament.total_registered_players),
                "remarks": tournament.remarks,            
                "registered_players": registered_players,
                "rounds" : rounds            
        }
        except FileNotFoundError as e:
            print(f"{e}")
        
    def _deserialize(self, data):
        tournament =  Tournament(
            id=data["id"],
            name=data["name"],
            location=data["location"],
            start_date=QDateTime.fromString(data["start_date"], Qt.ISODate),
            end_date=QDateTime.fromString(data["end_date"], Qt.ISODate),
            num_rounds=data["num_rounds"],
            current_round=data["current_round"],
            remarks=data["remarks"]
        )       
        tournament.total_registered_players = data["total_registered_players"]
          
        registered_players = []    
        for player in data["registered_players"]:
            registered_players.append(self.deserialize_player(player))
        tournament.registered_players = registered_players
        
        rounds = []
        for round in data["rounds"]:
            rounds.append(self._round_model.deserialize(round))
        tournament.rounds = rounds
            
        return tournament