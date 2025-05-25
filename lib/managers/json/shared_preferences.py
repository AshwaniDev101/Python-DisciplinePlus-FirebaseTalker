import json
import os

class SharedPreferences:
    _data = None
    _file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_data.json")



    @classmethod
    def _ensure_loaded(cls):
        if cls._data is None:
            os.makedirs(os.path.dirname(cls._file), exist_ok=True)
            if os.path.exists(cls._file):
                try:
                    with open(cls._file, "r") as f:
                        cls._data = json.load(f)
                except json.JSONDecodeError:
                    cls._data = {}
            else:
                cls._data = {}

    @classmethod
    def get(cls, key, default=None):
        cls._ensure_loaded()
        return cls._data.get(key, default)

    @classmethod
    def set(cls, key, value):
        cls._ensure_loaded()
        cls._data[key] = value
        cls._save()

    @classmethod
    def remove(cls, key):
        cls._ensure_loaded()
        if key in cls._data:
            del cls._data[key]
            cls._save()

    @classmethod
    def _save(cls):
        with open(cls._file, "w") as f:
            json.dump(cls._data, f, indent=4)
