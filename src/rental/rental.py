import json
import os
import uuid
import re
import datetime


class Rental:
    def __init__(self, database=None):
        if database:
            self._database = database
        else:
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
        for date_time_string in [date_time_from_string, date_time_to_string]:
            if not re.search('^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) ([0-1][0-9]|2[0-3]):[0-5][0-9]$', date_time_string):
                raise ValueError('Wrong date syntax')
            year_string, month_string, day_string = date_time_string.split(' ')[0].split('-')
            leap_modifier = 0
            if (int(year_string) % 400 == 0) or ((int(year_string) % 4 == 0) and (int(year_string) % 100 != 0)):
                leap_modifier += 1
            if month_string == '02' and int(day_string) > (28 + leap_modifier)\
                    or month_string in ['04', '06', '09', '11'] and day_string == '31':
                raise ValueError('No such day in provided month')

        if type(user_id) != str:
            raise TypeError('User ID must be a string')
        if user_id not in map(lambda user: user['id'], self._database['users']):
            raise LookupError('No such user')

        date_time_from, date_time_to = list(map(lambda date_time_string: datetime.datetime.strptime(date_time_string, '%Y-%m-%d %H:%M'), [date_time_from_string, date_time_to_string]))
        if date_time_from.minute % 30 != 0 or date_time_to.minute % 30 != 0:
            raise ValueError('Both dates must be rounded to full hours or half (:00/:30)')
        if (date_time_to - date_time_from).total_seconds() <= 0:
            raise ValueError('End date must be later than start date')

        weekday_from = self._database['open_hours'][date_time_from.weekday()]
        weekday_to = self._database['open_hours'][date_time_to.weekday()]
        if not weekday_from['is_open']\
                or not weekday_to['is_open']\
                or (datetime.timedelta(hours=date_time_from.hour, minutes=date_time_from.minute) - datetime.timedelta(hours=weekday_from['open'])).total_seconds() < 0:
            raise ValueError('Rental shop is closed during this time')

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
