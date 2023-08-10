from PySide2.QtWidgets import QMainWindow

class BaseController:
    def __init__(self, view_class):
        self.view = view_class()

    def show_view(self):
        self.view.show()
