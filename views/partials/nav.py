from views.home_view import HomeView
from views.tournament_creation_view import TournamentCreationView
from views.tournament_read_view import TournamentReadView
from views.tournament_manager_view import TournamentManagerView
from views.player_creation_view import PlayerCreationView
from views.player_read_view import PlayerReadView
from controllers.tournament_controller import TournamentController

class Nav:
    def __init__(self, base_view):
        self._base_view = base_view

    def switch_to_home(self):
        home_view = HomeView(self)
        self._base_view.switch_view(home_view, "Chess Manager - Home")

    def switch_to_tournament_creation(self):
        tournament_creation_view = TournamentCreationView(self)
        self._base_view.switch_view(tournament_creation_view, "Chess Manager - Tournament creation")
        
    def switch_to_tournament_read(self):
        # tournament_controller = TournamentController(self)
        # tournament_data = tournament_controller.data_repository._read_data_from_file()

        tournament_read_view = TournamentReadView(self)
        self._base_view.switch_view(tournament_read_view, "Chess Manager - Tournament view")
        
    def switch_to_tournament_manager(self, tournament):
        tournament_manager_view = TournamentManagerView(self, tournament)
        self._base_view.switch_view(tournament_manager_view, "Chess Manager - Tournament manager")
        
    def switch_to_player_creation(self):
        player_creation_view = PlayerCreationView(self)
        self._base_view.switch_view(player_creation_view, "Chess Manager - Player creation")
        
    def switch_to_player_read(self):
        player_read_view = PlayerReadView(self)
        self._base_view.switch_view(player_read_view, "Chess Manager - Player view")
