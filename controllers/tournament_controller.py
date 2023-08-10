from . import BaseController
from views.tournament_view import TournamentView

class TournamentController(BaseController):
    def __init__(self):
        super().__init__(TournamentView)

