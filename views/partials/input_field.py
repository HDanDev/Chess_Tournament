from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QDateTimeEdit, QTextEdit, QComboBox, QDateEdit
from PySide6.QtCore import QDateTime, QDate, QTime
from PySide6.QtGui import QIntValidator

class FormType:
    Normal = "normal"
    Numerical = "numerical"
    DateTime = "date_time"
    Date = "date"
    LongText = "text"
    Combo = "combo"

class InputField(QWidget):
    def __init__(self, layout, label, placeholder="", form_type="normal") -> None:
        self._layout = layout
        self._label = label
        self._placeholder = placeholder
        self._form_type = form_type
        self._input = None
            
        label = QLabel(self._label)
        label.setObjectName(f"label-{label}")
        self._layout.addWidget(label)
        self._input = self.create_component(self, self._form_type)
        self._input.setObjectName(f"input-{self._input}")
        self._layout.addWidget(self._input)
        
    @staticmethod
    def create_component(self, form_type):
        if form_type == FormType.Normal:
            input = QLineEdit()
            input.setPlaceholderText(self._placeholder)
            return input
        elif form_type == FormType.Numerical:
            input = QLineEdit()
            input.setValidator(QIntValidator())
            input.setPlaceholderText(self._placeholder)
            return input
        elif form_type == FormType.DateTime:
            input = QDateTimeEdit()
            min_datetime = QDateTime.currentDateTime()
            max_datetime = QDateTime.currentDateTime().addYears(15)
            input.setDateTimeRange(min_datetime, max_datetime)
            input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
            input.setDateTime(min_datetime)
            return input
        elif form_type == FormType.Date:
            age_limit = QDate.currentDate().addYears(-10)
            input = QDateEdit()
            input.setDisplayFormat("yyyy-MM-dd")
            input.setCalendarPopup(True)
            input.setDateRange(QDate(1900, 1, 1), age_limit)
            input.setDate(QDate(2000, 1, 1))
            return input
        elif form_type == FormType.LongText:
            input = QTextEdit()
            return input
        elif form_type == FormType.Combo:
            input = QComboBox()
            return input
        
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
           
    @property
    def form_type(self):
        return self._form_type

    @form_type.setter
    def form_type(self, value):
        self._form_type = value.lower() 
                  
    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = value