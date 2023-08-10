import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class BaseView(QMainWindow):
    def __init__(self, template_data):
        super().__init__()
        self.setWindowTitle(template_data["title"])
        self.setGeometry(100, 100, 400, 300)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        title_label = QLabel(template_data["title"])
        content_label = QLabel(template_data["content"])

        layout.addWidget(title_label)
        layout.addWidget(content_label)

def render_view(template_data):
    app = QApplication(sys.argv)
    window = BaseView(template_data)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    template_data = {
        "title": "Hello, PySide!",
        "content": "This is a simple rendering example.",
    }
    render_view(template_data)
