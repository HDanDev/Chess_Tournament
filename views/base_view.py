from PySide2.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton

class BaseView(QMainWindow):
    def __init__(self, controller, template_data=None):
        super().__init__()
        self.controller = controller
        self.template_data = template_data or {}

        self.setWindowTitle(self.template_data.get("title", "Untitled"))
        self.setGeometry(100, 100, 400, 300)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        title_label = QLabel(self.template_data.get("title", "Untitled"))
        content_label = QLabel(self.template_data.get("content", ""))

        layout.addWidget(title_label)
        layout.addWidget(content_label)

        self.setup_buttons(layout)

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