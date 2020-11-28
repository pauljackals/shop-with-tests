import json
import os


class Rental:
    def __init__(self):
        self._database = {}

    def load_database(self, database_file='database.json'):
        if type(database_file) != str:
            raise TypeError('Database file name must be a string')
        if not os.path.exists('../data/'+database_file):
            raise FileNotFoundError("Database doesn't exist")
        with open('../data/' + database_file) as file:
            self._database = json.loads(file.read())
        return True
