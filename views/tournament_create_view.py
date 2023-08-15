from .base_view import BaseView

class TournamentCreateView(BaseView):
    def __init__(self, controller):
        template_data = {
            "buttons": [
                {"text": "Create", "geometry": (50, 50, 30, 30)},
                {"text": "Create2", "geometry": (160, 50, 30, 30)},
                {"text": "Read", "geometry": (50, 100, 30, 30)},
                {"text": "Exit", "geometry": (160, 100, 30, 30)}
            ],
            "inputs": [
                {"label": "Create", "placeholder": "default value"},
                {"label": "Create2", "placeholder": "default value"},
                {"label": "Read", "placeholder": "default value"},
                {"label": "Exit", "placeholder": "default value"}
            ]
        }
        super().__init__(controller, "create", "create", "create", template_data)
        self._page_change("nouyveau titre", "nouveau test", "nouveau contenu")        
        self._add_input_field(self._content_layout)
        self._setup_buttons(self._content_layout)
        
    def create_new_tournament(self):
        self._page_change("nouyveau titre", "nouveau contenu")        
        self._add_input_field(self._content_layout)
        self._setup_buttons(self._content_layout)
        