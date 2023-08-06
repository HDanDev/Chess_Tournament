class Player:
    def __init__(self, last_name, first_name, date_of_birth, chess_id):
        self._last_name = last_name
        self._first_name = first_name
        self._date_of_birth = date_of_birth
        self._chess_id = chess_id

    def get_full_name(self):
        return f"{self._first_name} {self._last_name}"

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
        self._chess_id = value