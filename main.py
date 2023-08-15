import sys
from PySide2.QtWidgets import QApplication
from controllers.home_controller import HomeController

def main():
    app = QApplication(sys.argv)
    home_controller = HomeController()
    home_controller._show_view()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
