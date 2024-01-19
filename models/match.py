from enum import Enum
from repositories.player_repository import PlayerRepository


class MatchResult(Enum):
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"

    def serialize(self):
        return self.value

    @classmethod
    def deserialize(cls, value):
        if value == "win":
            return cls.WIN
        elif value == "lose":
            return cls.LOSE
        elif value == "draw":
            return cls.DRAW
        else:
            raise ValueError("Invalid MatchResult value")


class Match:
    def __init__(self, player1=None, player2=None, result=None):
        self._player1 = player1
        self._player2 = player2
        self._result = result
        self._winning_points = 1
        self._losing_points = 0
        self._draw_points = 0.5
        self._player_repository = PlayerRepository()
        self._score = []

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
        self._score = self.get_match_result()

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    def get_winner(self):
        try:
            if self._result == MatchResult.WIN:
                return self._player1.get_full_name()
            elif self._result == MatchResult.LOSE:
                return self._player2.get_full_name()
            else:
                return "Draw"
        except Exception as e:
            print(
                f"Could not retrieve the result for the "
                f"specified match probably because the "
                f"said match has no result yet: {e}"
            )

    def get_match_result(self):
        try:
            if self._result == MatchResult.WIN:
                return (
                    [self._player1, self._winning_points],
                    [self._player2, self._losing_points],
                )
            elif self._result == MatchResult.LOSE:
                return (
                    [self._player1, self._losing_points],
                    [self._player2, self._winning_points],
                )
            else:
                return (
                    [self._player1, self._draw_points],
                    [self._player2, self._draw_points],
                )
        except Exception as e:
            print(
                f"Could not retrieve the result for the "
                f"specified match probably because "
                f"the said match has no result yet: {e}"
            )

    def get_score_tuple(self, isWinner):
        try:
            if isWinner:
                return self.get_match_result()[0]
            else:
                return self.get_match_result()[1]
        except Exception as e:
            print(
                f"Could not retrieve the result for "
                f"the specified match probably because "
                f"the said match has no result yet: {e}"
            )

    def get_match_name(self):
        return (
            self._player1.get_full_name()
            + " vs " +
            self._player2.get_full_name()
        )

    def serialize(self):
        return {
            "player1": self._player_repository.serialize_player(self.player1),
            "player2": self._player_repository.serialize_player(self.player2),
            "result": self.result.serialize(),
        }

    def deserialize(self, data):
        new_match = Match()
        new_match.player1 = self._player_repository.deserialize_player(
            data["player1"]
            )
        new_match.player2 = self._player_repository.deserialize_player(
            data["player2"]
            )
        new_match.result = MatchResult.deserialize(data["result"])
        return new_match
