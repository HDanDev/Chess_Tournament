class Tournament:
    def __init__(self, name, location, start_date, end_date, num_rounds=4):
        self._name = name
        self._location = location
        self._start_date = start_date
        self._end_date = end_date
        self._num_rounds = num_rounds
        self._current_round = 1
        self._rounds = []
        self._registered_players = []
        self._infos = ""

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
        if 1 <= value <= self._num_rounds:
            self._current_round = value
        else:
            raise ValueError("Invalid round number. Must be between 1 and the number of rounds.")

    @property
    def rounds(self):
        return self._rounds

    @rounds.setter
    def rounds(self, value):
        self._rounds = value

    @property
    def registered_players(self):
        return self._registered_players

    @registered_players.setter
    def registered_players(self, value):
        self._registered_players = value

    @property
    def infos(self):
        return self._infos

    @infos.setter
    def infos(self, value):
        self._infos = value
