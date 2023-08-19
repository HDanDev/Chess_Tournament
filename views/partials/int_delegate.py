from PySide6.QtWidgets import QItemDelegate, QSpinBox
from PySide6.QtCore import Qt

class IntDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, editor, index):
        int_value = index.data(Qt.EditRole)
        editor.setValue(int_value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.value(), Qt.EditRole)
