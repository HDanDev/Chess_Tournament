import sys
from PySide6.QtWidgets import QApplication
from views.base_view import BaseView
from views.home_view import HomeView

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.base_view = BaseView(self.app)
        
    def run(self):
        self.base_view.show()
        home_view = HomeView(self)
        self.base_view.switch_view(home_view, "Chess Manager - Home")
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = MainApp()
    app.run()
