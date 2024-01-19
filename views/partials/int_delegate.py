from PySide6.QtWidgets import QItemDelegate, QSpinBox
from PySide6.QtCore import Qt


class IntDelegate(QItemDelegate):
    def __init__(self, parent=None, min_value=1, max_value=100):
        super().__init__(parent)
        self.min_value = min_value
        self.max_value = max_value

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setMinimum(self.min_value)
        editor.setMaximum(self.max_value)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(int(value))

    def setModelData(self, editor, model, index):
        value = editor.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
