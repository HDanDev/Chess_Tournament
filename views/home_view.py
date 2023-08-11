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
            ]
        }
        super().__init__(controller, template_data)
