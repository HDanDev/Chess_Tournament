from PySide6.QtWidgets import QItemDelegate, QDateTimeEdit
from PySide6.QtCore import QDateTime, Qt

class DateDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QDateTimeEdit(parent)
        editor.setDisplayFormat("ddd MMM dd hh:mm:ss yyyy")
        editor.setDateTime(QDateTime.currentDateTime())
        return editor

    def setEditorData(self, editor, index):
        date_value = index.data(Qt.EditRole)
        editor.setDateTime(date_value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.dateTime(), Qt.EditRole)
