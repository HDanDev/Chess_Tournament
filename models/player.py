import re 
import json
import string
import random

class Player:
    def __init__(self, last_name="", first_name="", date_of_birth="", chess_id=""):
        self._last_name = last_name
        self._first_name = first_name
        self._date_of_birth = date_of_birth
        self._chess_id = chess_id
        self._points = {}

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
        if self.is_null_or_white_space(value):
            self._chess_id = self.generate_chess_id()
        else:
            if not re.match(r'^[A-Za-z]{2}\d{5}$', value):
                raise ValueError("The chess ID should match the two letters followed by five numbers mandatory format.")

            self._chess_id = value.upper()
            
    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    def get_full_name(self):
        return f"{self._first_name} {self._last_name} ({self._chess_id})"
    
    def get_points(self, tournament_id):
        return self.points.get(tournament_id, 0)     
    
    def update_points(self, tournament_id, score):
        if tournament_id not in self.points:
            self.points[tournament_id] = 0
        self.points[tournament_id] = float(self.points[tournament_id]) + float(score)
    
    @staticmethod
    def is_null_or_white_space(string):
        return string is None or len(string.strip()) == 0
    
    @staticmethod    
    def generate_chess_id():
        letters = ''.join(random.choice(string.ascii_letters) for _ in range(2))
    
        digits = ''.join(random.choice(string.digits) for _ in range(5))
    
        chess_id = (letters + digits).upper()
    
        return chess_id