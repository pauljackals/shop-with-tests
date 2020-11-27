import json


class Rental:
    def __init__(self):
        self.database = {}

    def load_database(self):
        with open('../data/database.json') as file:
            self.database = json.loads(file.read())
        return True
