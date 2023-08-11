from . import BaseController
from views.home_view import HomeView

class HomeController(BaseController):
    def __init__(self):
        super().__init__(HomeView)

    def handle_button_click(self, button_text):
        if button_text == "Create":
            self.handle_create_button()
        elif button_text == "Create2":
            self.handle_create2_button()
        elif button_text == "Read":
            self.handle_read_button()
        elif button_text == "Exit":
            self.view.close()

    def handle_create_button(self):
        print("Create button clicked")

    def handle_create2_button(self):
        print("Create2 button clicked")

    def handle_read_button(self):
        print("Read button clicked")