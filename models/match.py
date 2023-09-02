from enum import Enum

class MatchResult(Enum):
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"

class Match:
    def __init__(self, player1=None, player2=None, result=None):
        self._player1 = player1
        self._player2 = player2
        self._result = result
        self._winning_points = 1
        self._losing_points = 0
        self._draw_points = 0.5

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
        
    def get_match_result(self):
        try: 
            if self._result == MatchResult.WIN:
                return ([self._player1, self._winning_points], [self._player2, self._losing_points])
            elif self._result == MatchResult.LOSE:
                return ([self._player1, self._losing_points], [self._player2, self._winning_points])
            else:
                return ([self._player1, self._draw_points], [self._player2, self._draw_points])
        except Exception as e:
            print(f"Could not retrieve the result for the specified match probably because the said maych has no result yet: {e}")
            
    def get_match_name(self):
        return self._player1.get_full_name() + " vs " + self._player2.get_full_name()