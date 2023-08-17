from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView
from controllers.tournament_controller import TournamentController

class TournamentReadView(QWidget):
    def __init__(self, main_app, user_data):
        super().__init__()

        self.main_app = main_app
        self.user_controller = TournamentController(main_app, user_data)

        self.layout = QVBoxLayout()

        self.label = QLabel("User List")
        self.layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Username", "Password"])
        self.table.itemChanged.connect(self.handle_item_changed)    

        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        
        self.user_controller.setup_view(self)

    def populate_table(self, user_data):
        for user in user_data:
            username = user["username"]
            password = user["password"]
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(username))
            self.table.setItem(row_position, 1, QTableWidgetItem(password))
            
    def handle_item_changed(self, item):
        self.user_controller.save_changes()