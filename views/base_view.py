from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QAction, QMenuBar, QLabel, QVBoxLayout, QWidget, QPushButton, QMenu, QHBoxLayout

class BaseView(QMainWindow):
    def __init__(self, controller, template_data=None):
        super().__init__()
        
        self.controller = controller
        self.template_data = template_data or {}
        
        self.init_ui()
        
    def init_ui(self):        

        self.setWindowTitle(self.template_data.get("name", "Chess Manager"))
        self.setGeometry(100, 100, 960, 540)
        menubar = self.menuBar()  
        
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
        # create_new_player_icon = QAction(QIcon("./assets/img/CVPortrait.png"), "Create New", self)
        player_menu.addAction(create_new_player)
        player_menu.addAction(see_player_list)
        # player_menu.addAction(create_new_player_icon)
        
        self.menuBr= QMenuBar(menubar)
        menubar.setCornerWidget(self.menuBr, Qt.TopRightCorner)
        self.home_btn = QMenu(self.menuBr)
        self.home_btn.setTitle("Menu")
        self.menuBr.addAction(self.home_btn.menuAction())
        
        # menu_widget = QWidget(self)
        # menu_layout = QVBoxLayout(menu_widget)
        # menu_layout.setMargin(100)
        # menu_button = QPushButton("Menu", self)
        # menu_button.clicked.connect(self.button_clicked)
        # menu_layout.addWidget(menu_button)
        
        # menu_button = QPushButton("Menu", self)
        # menu_icon = QIcon("./assets/img/CVPortrait.png")
        # menu_button.setIcon(menu_icon)
        
        # menubar.setCornerWidget(test_menu, Qt.TopRightCorner)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(0)
        main_layout.setMargin(0)

        title_label = QLabel(self.template_data.get("title", "untitled"))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        main_layout.addWidget(title_label)
        
        content_layout = QVBoxLayout()
        img_layout = QHBoxLayout()
        
        img_label = QLabel(self)
        img_label.setObjectName("img")
        pixmap = QPixmap("./assets/img/CVPortrait.png")
        img_label.setPixmap(pixmap)
        img_label.setScaledContents(True)
        img_label.setAlignment(Qt.AlignHCenter)
        img_layout.addWidget(img_label)        
        content_layout.addLayout(img_layout)

        main_content = QLabel(self.template_data.get("content", "N/A"))
        main_content.setAlignment(Qt.AlignCenter)
        main_content.setObjectName("content")
        content_layout.addWidget(main_content)

        main_layout.addLayout(content_layout)       

    def setup_buttons(self, layout):
        buttons_data = self.template_data.get("buttons", [])
        for button_info in buttons_data:
            button = QPushButton(button_info["text"], self)
            button.setGeometry(*button_info["geometry"])
            layout.addWidget(button)
            button.clicked.connect(self.button_clicked)
            
    def button_clicked(self):
        sender = self.sender() 
        self.controller.handle_button_click(sender.text())