from .base_view import BaseView

class HomeView(BaseView):
    def __init__(self, controller):
        template_data = {
            "title": "Hello, PySide!",
            "content": "This is a simple rendering example.",
            "buttons": [
                {"text": "Create", "geometry": (50, 50, 100, 30)},
                {"text": "Create2", "geometry": (160, 50, 100, 30)},
                {"text": "Read", "geometry": (50, 100, 100, 30)},
                {"text": "Exit", "geometry": (160, 100, 100, 30)}
            ],
            "inputs": [
                {"label": "Create", "placeholder": "default value"},
                {"label": "Create2", "placeholder": "default value"},
                {"label": "Read", "placeholder": "default value"},
                {"label": "Exit", "placeholder": "default value"}
            ]
        }
        super().__init__(controller, template_data)
        self.add_input_field(self._content_layout)
        self.setup_buttons(self._content_layout)
