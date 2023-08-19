from . import BaseRepository
from models.tournament import Tournament
import json

class TournamentRepository(BaseRepository):
    TOURNAMENT_JSON_FILE_PATH = './data/tournaments/tournaments_data.json'
    
    def __init__(self, file_path = TOURNAMENT_JSON_FILE_PATH):
        super().__init__(file_path)
        self.tournament = Tournament("","","","")
        
    def _read_json(self):
        tournaments = []
        try:
            with open(self.file_path, 'r') as file:
                deserialized_tournaments = json.load(file)
                for data in deserialized_tournaments:
                    tournaments.append(Tournament.deserialize_tournament(data))
        except FileNotFoundError as e:
            print(f"Could not find the file: {e}")
        return tournaments

        
    def _write_json(self, tournaments):
        try:
            serialized_tournaments = [tournament.serialize_tournament() for tournament in tournaments]
            with open(self.file_path, 'w') as file:
                json.dump(serialized_tournaments, file, indent=4)
        except FileNotFoundError as e:
            print(f"Could not find the file: {e}")

    def _update_json(self, tournament):
        try:
            data = self._read_json()

            for i, item in enumerate(data):
                if item.id == tournament.id:
                    data[i] = tournament
                    break

            with open(self.file_path, 'w') as file:
                serialized_data = [item.serialize_tournament() for item in data]
                json.dump(serialized_data, file, indent=4)
        except FileNotFoundError:
            print(f"Could not find the file: {self.file_path}")
            
    def _add_json(self, tournament):
        try:
            serialized_tournament = tournament.serialize_tournament()
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(serialized_tournament)

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)