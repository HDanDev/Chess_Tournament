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
            
    def clear_json(self):
        try:
            with open(self._file_path, 'r') as file:
                data = json.load(file)
            data.clear()

            with open(self._file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print("All entries cleared from the JSON file.")
            
        except FileNotFoundError as e:
            print(f"Could not find the file: {e}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON data in file: {self._file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def read_json(self):
        data = []
        try:
            with open(self._file_path, 'r') as file:
                deserialized_data = json.load(file)
                for item in deserialized_data:
                    data.append(self._deserialize(item))
        except FileNotFoundError as e:
            print(f"Could not find the file: {e}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON data in file: {self._file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return data
        
    def write_json(self, data):
        try:
            serialized_data = [self._serialize(item) for item in data]
            with open(self._file_path, 'w') as file:
                json.dump(serialized_data, file, indent=4)
        except FileNotFoundError as e:
            print(f"Could not find the file: {e}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON data in file: {self._file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
              

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
        except json.JSONDecodeError:
            print(f"Error decoding JSON data in file: {self._file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
            
    def delete_json(self, id):
        try:
            data = self.read_json()

            for i, item in enumerate(data):
                if getattr(item, self._attribute) == id:
                    data.remove(item)
                    break

            with open(self._file_path, 'w') as file:
                serialized_data = [self._serialize(item) for item in data]
                json.dump(serialized_data, file, indent=4)
        except FileNotFoundError:
            print(f"Could not find the file: {self._file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON data in file: {self._file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        

    def find_one_by_id(self, target_id):
        try:
            with open(self._file_path, "r") as f:
                data = json.load(f)
                for entry in data:
                    if entry[self._attribute] == target_id:
                        return self._deserialize(entry)
        except EntryNotFoundError as e:
            print(f"Could not find the element: {e}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON data in file: {self._file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
            return None     
            
    @staticmethod    
    def _deserialize(json_obj):
        pass
    
    @staticmethod    
    def _serialize(obj):
        pass