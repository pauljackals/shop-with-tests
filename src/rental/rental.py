import json


class Rental:
    def __init__(self):
        self.database = {}

    def load_database(self, database_file='database.json'):
        with open('../data/' + database_file) as file:
            self.database = json.loads(file.read())
        return True
