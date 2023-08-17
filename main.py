import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from views.base_view import BaseView
from views.home_view import HomeView
from views.tournament_creation_view import TournamentCreationView
from views.tournament_read_view import TournamentReadView
from views.player_creation_view import PlayerCreationView
from views.player_read_view import PlayerReadView
from controllers.tournament_controller import TournamentController

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.base_view = BaseView(self, self.app)
        
    def run(self):
        self.base_view.show()
        self.switch_to_home()
        sys.exit(self.app.exec())

    def switch_to_home(self):
        view1 = HomeView(self)
        self.base_view.switch_view(view1, "Chess Manager - Home")

    def switch_to_tournament_creation(self):
        tournament_creation_view = TournamentCreationView(self)
        self.base_view.switch_view(tournament_creation_view, "Chess Manager - Trournament creation")
        
    def switch_to_tournament_read(self):
        tournament_controller = TournamentController(self)
        tournament_data = tournament_controller.data_repository._read_data_from_file()

        tournament_read_view = TournamentReadView(self, tournament_data)
        self.base_view.switch_view(tournament_read_view, "Chess Manager - Trournament view")
        
    def switch_to_player_creation(self):
        player_creation_view = PlayerCreationView(self)
        self.base_view.switch_view(player_creation_view, "Chess Manager - Player creation")
        
    def switch_to_player_read(self):
        player_read_view = PlayerReadView(self)
        self.base_view.switch_view(player_read_view, "Chess Manager - Player view")

if __name__ == "__main__":
    app = MainApp()
    app.run()
