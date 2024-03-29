from views.home_view import HomeView
from views.tournament_creation_view import TournamentCreationView
from views.tournament_read_view import TournamentReadView
from views.tournament_manager_view import TournamentManagerView
from views.tournament_simulator_view import TournamentSimulatorView
from views.tournament_manager_picker_view import TournamentManagerPickerView
from views.player_creation_view import PlayerCreationView
from views.player_read_view import PlayerReadView
from views.round_read_view import RoundReadView
from views.tournament_step_by_step_simulator_view import (
    TournamentStepByStepSimulatorView,
)
from views.round_manager_view import RoundManager


class Nav:
    def __init__(self, base_view):
        self._base_view = base_view

    def switch_to_home(self):
        home_view = HomeView(self)
        self._base_view.switch_view(home_view, "Chess Manager - Home")

    def switch_to_tournament_creation(self):
        tournament_creation_view = TournamentCreationView(self)
        self._base_view.switch_view(
            tournament_creation_view, "Chess Manager - Tournament creation"
        )

    def switch_to_tournament_read(self):
        # tournament_controller = TournamentController(self)
        # tournament_data = (
        # tournament_controller.data_repository._read_data_from_file()
        # )

        tournament_read_view = TournamentReadView(self)
        self._base_view.switch_view(
            tournament_read_view, "Chess Manager - Tournament view"
        )

    def switch_to_tournament_manager(self, tournament, index=0):
        tournament_manager_view = TournamentManagerView(
            self,
            tournament,
            index
            )
        self._base_view.switch_view(
            tournament_manager_view,
            f'Chess Manager - Tournament manager - "{tournament.name}"',
        )

    def switch_to_tournament_picker_manager(self):
        tournament_simulator_picker_view = TournamentManagerPickerView(self)
        self._base_view.switch_view(
            tournament_simulator_picker_view,
            "Chess Manager - Tournament manager picker",
        )

    def switch_to_tournament_simulator(self, tournament):
        tournament_simulator_view = TournamentSimulatorView(self, tournament)
        self._base_view.switch_view(
            tournament_simulator_view,
            f'Chess Manager - Tournament simulator - "{tournament.name}"',
        )

    def switch_to_tournament_step_by_step_simulator(self, tournament):
        tournament_simulator_step_by_step_view = (
                TournamentStepByStepSimulatorView(
                    self,
                    tournament
                )
            )
        self._base_view.switch_view(
            tournament_simulator_step_by_step_view,
            f'Chess Manager - Tournament simulator - "{tournament.name}"',
        )

    def switch_to_round_manager(self, tournament):
        round_manager_view = RoundManager(self, tournament)
        self._base_view.switch_view(
            round_manager_view, f'Chess Manager - '
            f'Round manager - "{tournament.name}"'
        )

    def switch_to_player_creation(self):
        player_creation_view = PlayerCreationView(self)
        self._base_view.switch_view(
            player_creation_view, "Chess Manager - Player creation"
        )

    def switch_to_player_read(self):
        player_read_view = PlayerReadView(self)
        self._base_view.switch_view(
            player_read_view,
            "Chess Manager - Players view"
            )

    def switch_to_rounds_read(self, tournament):
        rounds_read_view = RoundReadView(self, tournament)
        self._base_view.switch_view(
            rounds_read_view,
            "Chess Manager - Rounds view"
            )
