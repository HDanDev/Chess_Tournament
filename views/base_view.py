from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QMenu, QMenuBar, QPushButton, QWidgetAction, QToolBar, QApplication
from PySide6.QtCore import Qt, QFile
from PySide6.QtGui import QPixmap, QIcon, QAction

class BaseView(QMainWindow):
    
    HOME_ICON = "./assets/img/home.png"
    APP_LOGO = "./assets/img/chess_logo.png"
    CHESS_IMG = "./assets/img/chess_img.png"
    
    def __init__(self, main_app, qapp):
        super().__init__()

        self.app = main_app
        self.qapp = qapp
        
        self.setGeometry(500, 200, 960, 540) 
        self.setWindowTitle("Chess Manager") 
        
        window_icon = QIcon(self.APP_LOGO)
        self.setWindowIcon(window_icon)
        
        self.central_widget = QWidget(self)        
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addSpacing(20)

        self._title = QLabel("")
        self._title.setAlignment(Qt.AlignCenter)
        self._title.setObjectName("title")
        self.main_layout.addWidget(self._title)
        self.main_layout.addSpacing(45)

        self._content_layout = QVBoxLayout()

        self.main_layout.addLayout(self._content_layout)
        self.main_layout.setAlignment(Qt.AlignTop)

        # self._label_input_map = {}

        self.load_stylesheet("./assets/css/styles.qss")

        self.setup_navigation_buttons()

    def switch_view(self, new_view, title):
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._content_layout.addWidget(new_view)
        new_view.show()
        
        self.setWindowTitle(title)
        self._title.setText(title) 
        
    def setup_navigation_buttons(self):
        menubar = self.menuBar()

        tournament_menu = menubar.addMenu("Tournament")
        tournament_menu.setObjectName("tournament-menu")

        switch_to_tournament_creation = QAction("Create", self)
        switch_to_tournament_read = QAction("View", self)
        switch_to_tournament_creation.triggered.connect(self.app.switch_to_tournament_creation)
        switch_to_tournament_read.triggered.connect(self.app.switch_to_tournament_read)
        tournament_menu.addAction(switch_to_tournament_creation)
        tournament_menu.addAction(switch_to_tournament_read)

        player_menu = menubar.addMenu("Player")
        player_menu.setObjectName("player-menu")

        switch_to_player_creation = QAction("Create", self)
        switch_to_player_read = QAction("View", self)
        switch_to_player_creation.triggered.connect(self.app.switch_to_player_creation)
        switch_to_player_read.triggered.connect(self.app.switch_to_player_read)
        player_menu.addAction(switch_to_player_creation)
        player_menu.addAction(switch_to_player_read)        
 
        switch_to_home = QPushButton(self)
        switch_to_home.setIcon(QIcon(self.HOME_ICON))
        switch_to_home.clicked.connect(self.app.switch_to_home)
        switch_to_home.setObjectName("home-btn")

        menubar.setCornerWidget(switch_to_home, corner=Qt.TopRightCorner)
        
    def load_stylesheet(self, filename):
        style_file = QFile(filename)
        if style_file.open(QFile.ReadOnly | QFile.Text):
            stylesheet = style_file.readAll().data().decode("utf-8")
            current_stylesheet = self.styleSheet()
            combined_stylesheet = current_stylesheet + stylesheet
            self.setStyleSheet(combined_stylesheet)