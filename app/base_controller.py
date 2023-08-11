class BaseController:
    def __init__(self, view_class):
        self.view = view_class(self)

    def show_view(self):
        self.view.show()

    def handle_button_click(self, button_text):
        pass