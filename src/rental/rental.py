import json
import os
import uuid


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

    def save_database(self):
        with open('../data/database_copy.json', 'w') as file:
            file.write(json.dumps(self._database))
        return True

    def get_user_reservations(self, id_user):
        if type(id_user) != str:
            raise TypeError('User ID must be a string')
        return list(filter(lambda reservation: reservation['user'] == id_user, self._database['reservations']))

    def create_reservation(self, user_id, game_id, date_time_from_string, date_time_to_string):
        new_reservation_id = str(uuid.uuid4())
        self._database['reservations'].append(
            {
                'id': new_reservation_id,
                'user': user_id,
                'game': game_id,
                'from': date_time_from_string,
                'to': date_time_to_string
            }
        )
        return new_reservation_id
