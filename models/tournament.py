import uuid
from PySide6.QtCore import QDateTime

class Tournament:
    def __init__(self, name="Untitled tournament", location="Undefined location", start_date="", end_date="", id="",num_rounds=4, current_round=1, remarks=""):
        self._id = id if id != "" else str(uuid.uuid4())
        self._name = name
        self._location = location
        self._start_date = start_date if start_date else QDateTime.currentDateTime()
        self._end_date = end_date if end_date else QDateTime.currentDateTime().addMonths(1)
        self._num_rounds = num_rounds
        self._current_round = current_round
        self._rounds = []
        self._registered_players = []
        self._total_registered_players = len(self.registered_players)
        self._remarks = remarks

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value 
    
    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value    

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    @property
    def num_rounds(self):
        return self._num_rounds  
        
    @num_rounds.setter
    def num_rounds(self, value):
        self._num_rounds = value

    @property
    def current_round(self):
        return self._current_round

    @current_round.setter
    def current_round(self, value):
        if 1 <= int(value) <= int(self._num_rounds):
            self._current_round = int(value)
        else:
            raise ValueError("Invalid round number. Must be between 1 and the number of rounds.")

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, value):
        if value: self._rounds = value    

    def add_round(self, round):
        self._rounds.append(round)

    def remove_round(self, round):
        self._rounds.remove(round)
        
    @property
    def registered_players(self):
        return self._registered_players

    @registered_players.setter
    def registered_players(self, value):
        self._registered_players = value
        
    @property
    def total_registered_players(self):
        return self._total_registered_players  
        
    @total_registered_players.setter
    def total_registered_players(self, value):
        self._total_registered_players = value
    
    # @registered_players.setter
    # def registered_players(self, value):
    #     if isinstance(value, list) and len(value) == 2:
    #         self._registered_players = value
    #     else:
    #         self._registered_players = [value, 0]

    def add_player(self, player):
        self._registered_players.append(player)
        self._total_registered_players = len(self.registered_players)

    def remove_player(self, player):
        self._registered_players.remove(player)
        self._total_registered_players = len(self.registered_players)        
        
    # def update_player_score(self, target_player, updated_score):
    #     for player in self._registered_players:
    #         entity, score = player
    #         if entity == target_player:
    #             player[1] = updated_score
    #             break        
        
    @property
    def remarks(self):
        return self._remarks

    @remarks.setter
    def remarks(self, value):
        if value: self._remarks = value
        
    def update_player_score(self, player, score):
        if player in self.registered_players:
            player.update_points(self.id, score)
        else:
            raise ValueError("Player is not registered for this tournament.")
