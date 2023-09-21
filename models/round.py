from PySide6.QtCore import Qt, QDateTime
from models.match import Match
class Round:
    def __init__(self, name="", start_datetime=None, end_datetime=None):
        self._name = name
        self._start_datetime = start_datetime
        self._end_datetime = end_datetime
        self._matches = []
        self._match_model = Match()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def start_datetime(self):
        return self._start_datetime

    @start_datetime.setter
    def start_datetime(self, value):
        self._start_datetime = value

    @property
    def end_datetime(self):
        return self._end_datetime

    @end_datetime.setter
    def end_datetime(self, value):
        self._end_datetime = value

    @property
    def matches(self):
        return self._matches

    @matches.setter
    def matches(self, value):
        self._matches = value

    def add_match(self, match):
        self._matches.append(match)

    def serialize(self):   
        matches = [] 
        if len(self.matches) > 0:
            for match in self.matches:
                matches.append(match.serialize())

        return {
            "name": self.name,
            "start_datetime": self.start_datetime.toString(Qt.ISODate),
            "end_datetime": self.end_datetime.toString(Qt.ISODate), 
            "matches": matches
        }
        
    def deserialize(self, data):  
        new_round = Round()
        matches = []
        for match in data["matches"]: 
            matches.append(self._match_model.deserialize(match))     

        new_round.name = data["name"]
        new_round.start_datetime = QDateTime.fromString(data["start_datetime"], Qt.ISODate)
        new_round.end_datetime = QDateTime.fromString(data["end_datetime"], Qt.ISODate)
        new_round.matches = matches      
        
        return new_round
