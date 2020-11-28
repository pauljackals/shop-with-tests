import json
import os
import uuid
import re


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
        if id_user not in list(map(lambda user: user['id'], self._database['users'])):
            raise LookupError('No such user')
        return list(filter(lambda reservation: reservation['user'] == id_user, self._database['reservations']))

    def create_reservation(self, user_id, game_id, date_time_from_string, date_time_to_string):
        if not re.search('^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) ([0-1][0-9]|2[0-3]):[0-5][0-9]$', date_time_from_string):
            raise ValueError('Wrong date syntax')
        year_from, month_from, day_from = date_time_from_string.split(' ')[0].split('-')
        leap_modifier = 0
        if (int(year_from) % 400 == 0) or ((int(year_from) % 4 == 0) and (int(year_from) % 100 != 0)):
            leap_modifier += 1
        if month_from == '02' and int(day_from) > (28 + leap_modifier)\
                or month_from in ['04', '06', '09', '11'] and day_from == '31':
            raise ValueError('No such day in provided month')

        if not re.search('^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) ([0-1][0-9]|2[0-3]):[0-5][0-9]$', date_time_to_string):
            raise ValueError('Wrong date syntax')
        year_to, month_to, day_to = date_time_to_string.split(' ')[0].split('-')
        leap_modifier = 0
        if (int(year_to) % 400 == 0) or ((int(year_to) % 4 == 0) and (int(year_to) % 100 != 0)):
            leap_modifier += 1
        if month_to == '02' and int(day_to) > (28 + leap_modifier)\
                or month_to in ['04', '06', '09', '11'] and day_to == '31':
            raise ValueError('No such day in provided month')

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
