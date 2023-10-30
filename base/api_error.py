
class MihoyoBBSException(Exception):
    def __init__(self, json_str):
        super().__init__(json_str)

