from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar, QLabel, QVBoxLayout, QWidget, QPushButton, QMenu, QHBoxLayout, QLineEdit

class BaseView(QMainWindow):
    def __init__(self, controller, template_data=None):
        super().__init__()
        
        self._controller = controller
        self._template_data = template_data or {}
        
        self._init_ui()
        
    def _init_ui(self):        

        self.setWindowTitle(self._template_data.get("name", "Chess Manager"))
        self.setGeometry(100, 100, 960, 540)
        menubar = self.menuBar() 
        self._label_input_map = {} 
        
        with open("./assets/css/styles.qss", "r") as css_file:
            self.setStyleSheet(css_file.read())
        
        tournament_menu = menubar.addMenu("Tournament")
        tournament_menu.setObjectName("tournament-dd")
        create_new_tournament = QAction("Create New", self)
        see_tournament_list = QAction("See List", self)
        tournament_menu.addAction(create_new_tournament)
        tournament_menu.addAction(see_tournament_list)
        
        player_menu = menubar.addMenu("Player")
        player_menu.setObjectName("player-dd")
        create_new_player = QAction("Create New", self)
        see_player_list = QAction("See List", self)
        # create_new_player_icon = QAction(QIcon("./assets/img/chess_logo.png"), "Create New", self)
        player_menu.addAction(create_new_player)
        player_menu.addAction(see_player_list)
        # player_menu.addAction(create_new_player_icon)
        
        menuBr= QMenuBar(menubar)
        menubar.setCornerWidget(menuBr, Qt.TopRightCorner)
        home_btn = QMenu(menuBr)
        home_btn.setTitle("Menu")
        menuBr.addAction(home_btn.menuAction())
        
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
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setMargin(0)

        title_label = QLabel(self._template_data.get("title", "untitled"))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        main_layout.addWidget(title_label)
        
        self._content_layout = QVBoxLayout()
        img_layout = QHBoxLayout()
        
        img_label = QLabel(self)
        img_label.setObjectName("img")
        pixmap = QPixmap("./assets/img/chess_logo.png")
        img_label.setPixmap(pixmap)
        img_label.setScaledContents(True)
        img_label.setAlignment(Qt.AlignHCenter)
        img_layout.addWidget(img_label)        
        self._content_layout.addLayout(img_layout)

        main_content = QLabel(self._template_data.get("content", "N/A"))
        main_content.setAlignment(Qt.AlignCenter)
        main_content.setObjectName("content")
        self._content_layout.addWidget(main_content)

        main_layout.addLayout(self._content_layout)       

    def setup_buttons(self, layout):
        buttons_data = self._template_data.get("buttons", [])
        for button_info in buttons_data:
            button = QPushButton(button_info["text"], self)
            button.setGeometry(*button_info["geometry"])
            layout.addWidget(button)
            button.clicked.connect(self.button_clicked)
            
    def add_input_field(self, layout):
        input_data = self._template_data.get("inputs", [])
        for input_info in input_data:
            label = QLabel(input_info["label"], self)
            input_field = QLineEdit(input_info["placeholder"], self)
            layout.addWidget(label)
            layout.addWidget(input_field)
            self._label_input_map[label] = input_field
            
    def button_clicked(self):
        sender = self.sender() 
        self._controller._handle_button_click(sender.text())
        
    # @property    
    # def get_template_data(self):
    #     return self._template_data
    
    # @property    
    # def label_input_map(self):
    #     return self._label_input_map