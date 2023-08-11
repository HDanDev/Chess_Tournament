import re 

class Player:
    def __init__(self, last_name, first_name, date_of_birth, chess_id):
        self._last_name = last_name
        self._first_name = first_name
        self._date_of_birth = date_of_birth
        self._chess_id = chess_id
        self._points = 0

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        self._date_of_birth = value

    @property
    def chess_id(self):
        return self._chess_id

    @chess_id.setter
    def chess_id(self, value):
        try:
            if re.match(r'^[A-Za-z]{2}\d{5}$', value):
                self._chess_id = value
            else:
                raise ValueError("The chess ID should match the two letters followed by five numbers mandatory format.")
        except ValueError as e:
            print(e)
            
    @property
    def points(self):
        return self.points

    @points.setter
    def points(self, value):
        self._points = value

    def get_full_name(self):
        return f"{self._first_name} {self._last_name} ({self._chess_id})"
        