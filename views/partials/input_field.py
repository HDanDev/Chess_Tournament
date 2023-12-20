from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QDateTimeEdit, QTextEdit, QComboBox, QDateEdit, QErrorMessage
from PySide6.QtCore import QDateTime, QDate, Signal
from PySide6.QtGui import QIntValidator
import re

class FormType:
    Normal = "normal"
    Numerical = "numerical"
    DateTime = "date_time"
    Date = "date"
    LongText = "text"
    Combo = "combo"
            
class ValidatingLineEdit(QLineEdit):
    onKeyUp = Signal()
    def keyReleaseEvent(self, event):
        # validate_input(self)
        # input_field = self.findInputFieldParent(self.parentWidget())
        # print(input_field)
        # if input_field:
        #     input_field.validate_input()
        self.returnPressed.emit()
            
    def findInputFieldParent(self, widget):
        if not widget:
            return None

        if isinstance(widget, InputField):
            return widget

        return self.findInputFieldParent(widget.parentWidget())
    
class InputField(QWidget):
    def __init__(self, layout, label, placeholder="", form_type="normal", is_mandatory=False, is_regex=False) -> None:
        super().__init__() 
        self._layout = layout
        self._label = label
        self._placeholder = placeholder
        self._form_type = form_type
        self._input = None
        self._error_message = QLabel()
        self._error_message.setVisible(False)
        self._error_message.setStyleSheet("color: red; font-weight: bold;")
        self._is_mandatory = is_mandatory
        self._is_regex = is_regex
        
        self._label = QLabel(self._label)
        self._label.setObjectName(f"label-{self._label}")
        self._layout.addWidget(self._label)
        self._input = self.create_component()
        self._input.setObjectName(f"input")
        self._layout.addWidget(self._input)
        self._layout.addWidget(self._error_message)
        
    def create_component(self):
        if self._form_type == FormType.Normal:
            input = ValidatingLineEdit()
            input.setPlaceholderText(self._placeholder)
            if self._is_mandatory or self._is_regex : input.returnPressed.connect(self.validate_input)
            return input
        elif self._form_type == FormType.Numerical:
            input = ValidatingLineEdit()
            int_validator = QIntValidator(self)
            int_validator.setBottom(1)
            input.setValidator(int_validator)
            input.setPlaceholderText(self._placeholder)
            input.returnPressed.connect(self.validate_input)
            return input
        elif self._form_type == FormType.DateTime:
            input = QDateTimeEdit()
            min_datetime = QDateTime.currentDateTime()
            max_datetime = QDateTime.currentDateTime().addYears(15)
            input.setDateTimeRange(min_datetime, max_datetime)
            input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
            input.setDateTime(min_datetime)
            return input
        elif self._form_type == FormType.Date:
            age_limit = QDate.currentDate().addYears(-10)
            input = QDateEdit()
            input.setDisplayFormat("yyyy-MM-dd")
            input.setCalendarPopup(True)
            input.setDateRange(QDate(1900, 1, 1), age_limit)
            input.setDate(QDate(2000, 1, 1))
            return input
        elif self._form_type == FormType.LongText:
            input = QTextEdit()
            return input
        elif self._form_type == FormType.Combo:
            input = QComboBox()
            return input

    def validate_input(self):
        value = self._input.text()
        if not self.is_valid(value):
            self.set_error()
            return False
        else:
            self.clear_error()
            return True

    def is_valid(self, value):
        if self._form_type == FormType.Numerical :
            try:
                int(value)
                if(int(value) > 0) :
                    return True
                else :
                    self._error_message.setText("Cannot be below 1")
                    return False
            except ValueError:
                self._error_message.setText("Only numbers are allowed in this field")
                return False
        else :
            if self._is_regex :
                string_length = len(value)

                patterns = {
                1: r'^[a-zA-Z]$',
                2: r'^[a-zA-Z]{2}$',
                3: r'^[a-zA-Z]{2}\d{1}$',
                4: r'^[a-zA-Z]{2}\d{2}$',
                5: r'^[a-zA-Z]{2}\d{3}$',
                6: r'^[a-zA-Z]{2}\d{4}$',
                }

                if string_length in patterns and not re.match(patterns[string_length], value):
                    self._error_message.setText("Pattern must match the \"LL0000\" format")
                    return False
                elif string_length > 6 : self._input.setText(str(value[:6]))  
                
            else :       
                is_not_whitespace = bool(re.search(r'\S', value))
                if(value is not None and is_not_whitespace) :
                    return True
                else :
                    self._error_message.setText("Cannot be empty")
                    return False
        return True
    
    def set_error(self):
        self._error_message.setVisible(True)
        self._input.setStyleSheet("border: 1px solid red;")

    def clear_error(self):
        self._error_message.setVisible(False)
        self._input.setStyleSheet("")
    
    def remove_widgets(self):
        self._layout.removeWidget(self._label)
        self._layout.removeWidget(self._input)
        
        self._label.deleteLater()
        self._input.deleteLater()
        
        self._label.setVisible(False)
        self._input.setVisible(False)        
        
    def show(self):
        self._label.setVisible(True)
        self._input.setVisible(True)

    def hide(self):
        self._label.setVisible(False)
        self._input.setVisible(False)
        
    def displace(self, index):
        self._layout.removeWidget(self._label)
        self._layout.removeWidget(self._input)
        
        self._layout.insertWidget(index, self._label)
        self._layout.insertWidget(index + 1, self._input)    
        
    def set_text(self, text):
        self._input.setText(str(text))    
        
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