class Match:
    def __init__(self, player1, player2, score=None):
        self._player1 = player1
        self._player2 = player2
        self._score = score

    @property
    def player1(self):
        return self._player1

    @player1.setter
    def player1(self, value):
        self._player1 = value

    @property
    def player2(self):
        return self._player2

    @player2.setter
    def player2(self, value):
        self._player2 = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if value is None or 0 <= value <= 1:
            self._score = value
        else:
            raise ValueError("Invalid score. Must be None or a value between 0 and 1.")
