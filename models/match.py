from enum import Enum

class MatchResult(Enum):
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"

class Match:
    def __init__(self, player1, player2, result=None):
        self._player1 = player1
        self._player2 = player2
        self._result = result

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
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value