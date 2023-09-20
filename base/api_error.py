import json


class MihoyoBBSException(Exception):
    def __init__(self, json_str):
        super().__init__(json.load(json_str))
