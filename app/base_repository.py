import json

class BaseRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def _read_data_from_file(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _write_data_to_file(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_all(self):
        return self._read_data_from_file()

    def add(self, entity):
        data = self._read_data_from_file()
        data.append(entity.__dict__)
        self._write_data_to_file(data)
