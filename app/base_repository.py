import json

class BaseRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def _read_json(self):
        pass

    def _write_json(self, data):
        pass

    def _get_all(self):
        return self._read_json()

    def _add_json(self, entity):
        pass
