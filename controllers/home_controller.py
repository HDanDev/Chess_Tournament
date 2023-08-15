from . import BaseController
from views.home_view import HomeView

class HomeController(BaseController):
    def __init__(self):
        super().__init__(HomeView)

    def _handle_button_click(self, button_text):
        if button_text == "Create":
            self._handle_create_button()
        elif button_text == "Create2":
            self._handle_create2_button()
        elif button_text == "Read":
            self._handle_read_button()
        elif button_text == "Exit":
            self.view.close()

    def _handle_create_button(self):
        self._get_input_data()

    def _handle_create2_button(self):
        print("Create2 button clicked")

    def _handle_read_button(self):
        print("Read button clicked")