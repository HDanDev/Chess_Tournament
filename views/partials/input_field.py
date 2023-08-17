from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout

class InputField(QWidget):
    def __init__(self, layout, label, placeholder="") -> None:
        self._layout = layout
        self._label = label
        self._placeholder = placeholder
        
        self.create_form()

    def create_form(self):
        label = QLabel(self._label)
        label.setObjectName(f"label-{label}")
        input = QLineEdit()
        input.setPlaceholderText(self._placeholder)
        input.setObjectName(f"input-{input}")

        self._layout.addWidget(label)
        self._layout.addWidget(input)
        
    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, value):
        self._layout = value    
            
    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value     
           
    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = value