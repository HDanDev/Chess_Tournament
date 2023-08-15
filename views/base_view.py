from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QLabel, QVBoxLayout, QWidget, QPushButton, QMenu, QHBoxLayout, QLineEdit
# from controllers.home_controller import HomeController
# from controllers.tournament_controller import TournamentController

class BaseView(QMainWindow):
    def __init__(self, controller, name="", title="", content="", template_data=None):
        super().__init__()
        
        self._controller = controller
        self._template_data = template_data or {}         
        self._name = name
        self._title = title
        self._content = content
        self._init_ui()
        
    def _init_ui(self):        

        self.setWindowTitle(self._name)
        self.setGeometry(100, 100, 960, 540)
        menubar = self.menuBar() 
        self._label_input_map = {}
        
        with open("./assets/css/styles.qss", "r") as css_file:
            self.setStyleSheet(css_file.read())
        
        tournament_menu = menubar.addMenu("Tournament")
        tournament_menu.setObjectName("tournament-dd")
        create_new_tournament = QAction("Create New", self)
        create_new_tournament.triggered.connect(self.create_new_tournament)
        see_tournament_list = QAction("See List", self)
        see_tournament_list.triggered.connect(self.see_tournament_list)
        tournament_menu.addAction(create_new_tournament)
        tournament_menu.addAction(see_tournament_list)
        
        player_menu = menubar.addMenu("Player")
        player_menu.setObjectName("player-dd")
        create_new_player = QAction("Create New", self)
        create_new_player.triggered.connect(self.create_new_player)
        see_player_list = QAction("See List", self)
        see_player_list.triggered.connect(self.see_player_list)
        # create_new_player_icon = QAction(QIcon("./assets/img/chess_logo.png"), "Create New", self)
        player_menu.addAction(create_new_player)
        player_menu.addAction(see_player_list)
        # player_menu.addAction(create_new_player_icon)
        
        menuBr= QMenuBar(menubar)
        menubar.setCornerWidget(menuBr, Qt.TopRightCorner)
        home_btn = QMenu(menuBr)
        home_btn.setTitle("Menu")
        home_action = home_btn.menuAction()
        menuBr.addAction(home_action)
        home_action.triggered.connect(self.home_button_clicked)
        
        # menu_widget = QWidget(self)
        # menu_layout = QVBoxLayout(menu_widget)
        # menu_layout.setMargin(100)
        # menu_button = QPushButton("Menu", self)
        # menu_button.clicked.connect(self.button_clicked)
        # menu_layout.addWidget(menu_button)
        
        # menu_button = QPushButton("Menu", self)
        # menu_icon = QIcon("./assets/img/chess_logo.png")
        # menu_button.setIcon(menu_icon)
        
        # menubar.setCornerWidget(test_menu, Qt.TopRightCorner)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addSpacing(20)

        self.title_label = QLabel(self._title)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("title")
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addSpacing(45)        
        
        self._content_layout = QVBoxLayout()
        self.main_img_layout = QHBoxLayout()
        self._content_layout.addLayout(self.main_img_layout)
        self._content_layout.addSpacing(45)

        self._main_content = QLabel(self._content)
        self._main_content.setAlignment(Qt.AlignCenter)
        self._main_content.setObjectName("content")
        self._content_layout.addWidget(self._main_content)

        self.main_layout.addLayout(self._content_layout)       
        self.main_layout.setAlignment(Qt.AlignTop)

    def _setup_buttons(self, layout):
        buttons_data = self._template_data.get("buttons", [])
        for button_info in buttons_data:
            button = QPushButton(button_info["text"], self)
            button.setGeometry(*button_info["geometry"])
            layout.addWidget(button)
            button.clicked.connect(self._button_clicked)
            
    def _add_input_field(self, layout):
        input_data = self._template_data.get("inputs", [])
        for input_info in input_data:
            label = QLabel(input_info["label"], self)
            input_field = QLineEdit(input_info["placeholder"], self)
            layout.addWidget(label)
            layout.addWidget(input_field)
            self._label_input_map[label] = input_field       
        
    def _set_img(self, layout, id="img", path="./assets/img/chess_logo.png"):
        img_label = QLabel(self)
        img_label.setObjectName(id)
        pixmap = QPixmap(path)
        img_label.setPixmap(pixmap)
        img_label.setScaledContents(True)
        img_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(img_label)        
            
    def _button_clicked(self):
        sender = self.sender() 
        self._controller._handle_button_click(sender.text())
        
    def create_new_tournament(self):
        # tournament_controller = TournamentController()
        # tournament_controller._show_view()
        pass

    def see_tournament_list(self):        
        # tournament_controller = TournamentController()
        # tournament_controller._show_list_tournament()
        pass

    def create_new_player(self):
        print("Create New Player clicked")

    def see_player_list(self):
        print("See Player List clicked")
        
    def home_button_clicked(self):
        # home_controller = HomeController()
        # home_controller._show_view()
        pass    
    
    def _page_change(self, name="", title="", content=""):
        self.setWindowTitle(name)
        self.title_label.setText(title)
        self._main_content.setText(content)
        self.setCentralWidget(self.central_widget)
        
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
    @property
    def label_input_map(self):
        return self._label_input_map

    @label_input_map.setter
    def label_input_map(self, value):
        self._label_input_map = value

    @property
    def name(self):
        return self._name

    @name.setter
    def title(self, value):
        self._name = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value