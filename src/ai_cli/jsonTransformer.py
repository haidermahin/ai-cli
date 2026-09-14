import re
from pydantic.alias_generators import to_snake


class JsonTransformer:
    def __init__(self):
        self.json_data = None

    def transform(self, json_data):
        normalized = {to_snake(key): value.strip() if isinstance(value, str) else value 
        for key, value in json_data.items()}

        if "event_name" not in normalized:
            raise ValueError("event_name is required")
        if "user_id" not in normalized:
            raise ValueError("user id is required")

        self.json_data = normalized
        return self.json_data

    def get_json_data(self):
        return self.json_data
