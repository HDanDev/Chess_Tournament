from PySide6.QtWidgets import QHBoxLayout, QCheckBox, QWidget
from PySide6.QtCore import Qt, Signal

class CenteredCheckBoxWidget(QWidget):
    stateChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        checkbox = QCheckBox()
        layout.addWidget(checkbox)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        checkbox.stateChanged.connect(self.emit_state_changed)

    def isChecked(self):
        checkbox = self.layout().itemAt(0).widget()
        return checkbox.isChecked()

    def setChecked(self, checked):
        checkbox = self.layout().itemAt(0).widget()
        checkbox.setChecked(checked)

    def emit_state_changed(self, state):
        self.stateChanged.emit(state)