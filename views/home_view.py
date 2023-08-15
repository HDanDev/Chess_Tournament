from .base_view import BaseView
from controllers.tournament_controller import TournamentController

class HomeView(BaseView):
    def __init__(self, controller):
        super().__init__(controller)
        self._add_input_field(self._content_layout)
        self._setup_buttons(self._content_layout)
        self._set_img(self.main_img_layout)
        self._page_change("Home","Welcome to Chess Manager","Welcome to your personal chess tournament manager")

    def create_new_tournament(self):
        self.clear_layout(layout=self.main_img_layout)
        self.clear_layout(layout=self._content_layout)
        tournament_controller = TournamentController()        
        tournament_controller.view._page_change(name="nouyveau titre", title="nouveau test", content="nouveau contenu")        
        tournament_controller.view._add_input_field(self._content_layout)
        tournament_controller.view._setup_buttons(self._content_layout)
        
        ### Popup a new window ###
        # tournament_controller = TournamentController()
        # tournament_controller._show_view()
        
            