import json

class EntryNotFoundError(Exception):
    pass

class BaseRepository:
    def __init__(self, file_path):
        self._file_path = file_path
        self._attribute = "id"

    def add_json(self, obj):
        try:
            serialized_obj = self._serialize(obj)
            with open(self._file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        data.append(serialized_obj)

        with open(self._file_path, "w") as file:
            json.dump(data, file, indent=4)       
        
    def read_json(self):
        data = []
        try:
            with open(self._file_path, 'r') as file:
                deserialized_data = json.load(file)
                for item in deserialized_data:
                    data.append(self._deserialize(item))
        except FileNotFoundError as e:
            print(f"Could not find the file: {e}")
        return data
        
    def write_json(self, data):
        try:
            serialized_data = [self._serialize(item) for item in data]
            with open(self._file_path, 'w') as file:
                json.dump(serialized_data, file, indent=4)
        except FileNotFoundError as e:
            print(f"Could not find the file: {e}")      

    def update_json(self, obj):
        try:
            data = self.read_json()

            for i, item in enumerate(data):
                if getattr(item, self._attribute) == getattr(obj, self._attribute):
                    data[i] = obj
                    break

            with open(self._file_path, 'w') as file:
                serialized_data = [self._serialize(item) for item in data]
                json.dump(serialized_data, file, indent=4)
        except FileNotFoundError:
            print(f"Could not find the file: {self._file_path}")
            
    def delete_json(self, obj):
        try:
            data = self.read_json()

            for item in enumerate(data):
                if getattr(item, self._attribute) == getattr(obj, self._attribute):
                    data.remove(item)
                    break

            with open(self._file_path, 'w') as file:
                serialized_data = [self._serialize(item) for item in data]
                json.dump(serialized_data, file, indent=4)
        except FileNotFoundError:
            print(f"Could not find the file: {self._file_path}")

    def find_one_by_id(self, target_id):
        try:
            with open(self._file_path, "r") as f:
                data = json.load(f)
                for entry in data:
                    if entry[self._attribute] == target_id:
                        return self._deserialize(entry)
        except EntryNotFoundError as e:
            print(f"Could not find the element: {e}")
            return None     
            
    @staticmethod    
    def _deserialize(json_obj):
        pass
    
    @staticmethod    
    def _serialize(obj):
        pass