from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox
from PySide6.QtCore import Qt
from repositories.tournament_repository import TournamentRepository, Tournament
from controllers.tournament_controller import TournamentController

class TournamentSimulatorPickerView(QWidget):
    def __init__(self, nav):
        super().__init__()

        self._nav = nav
        self.tournament_controller = TournamentController(self._nav)
        self._tournaments = self.tournament_controller.get_tournament_data()
        
        self.layout = QVBoxLayout()

        self.label = QLabel("Tournament Simulator")
        self.layout.addWidget(self.label)        

        self.combo_box = QComboBox()

        # model = self.combo_box.model()

        for tournament in self._tournaments:
            item = tournament.name
            self.combo_box.addItem(item)
            self.combo_box.setItemData(self.combo_box.count() - 1, tournament, role=Qt.UserRole)
            
        self.combo_box.setCurrentIndex(0)

        self.button = QPushButton("Simulate tournament")
        self.button.clicked.connect(self.select_tournament)

        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(self.button)
        # self.combo_box.currentIndexChanged.connect(self.select_tournament)
        
        self.setLayout(self.layout)
        
    def select_tournament(self):
        index = self.combo_box.currentIndex()
        selected_tournament = self.combo_box.itemData(index, role=Qt.UserRole)
        if selected_tournament:
            self._nav.switch_to_tournament_manager(selected_tournament, index)
        
        