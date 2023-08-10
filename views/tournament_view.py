from .base_view import BaseView

class TournamentView(BaseView):
    def __init__(self):
        template_data = {
            "title": "Hello, PySide!",
            "content": "This is a simple rendering example.",
        }
        super().__init__(template_data)

        # Customize the content for the tournament view
