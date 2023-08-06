class Round:
    def __init__(self, name, start_datetime=None, end_datetime=None):
        self._name = name
        self._start_datetime = start_datetime
        self._end_datetime = end_datetime
        self._matches = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def start_datetime(self):
        return self._start_datetime

    @start_datetime.setter
    def start_datetime(self, value):
        self._start_datetime = value

    @property
    def end_datetime(self):
        return self._end_datetime

    @end_datetime.setter
    def end_datetime(self, value):
        self._end_datetime = value

    @property
    def matches(self):
        return self._matches

    @matches.setter
    def matches(self, value):
        self._matches = value

    def add_match(self, match):
        self._matches.append(match)
