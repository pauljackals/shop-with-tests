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
        if id_user not in map(lambda user: user['id'], self._database['users']):
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
        if type(game_id) != int:
            raise TypeError('Game ID must be an integer')
        if game_id not in map(lambda game: game['id'], self._database['games']):
            raise LookupError('No such game')

        date_time_from, date_time_to = map(lambda date_time_string: datetime.datetime.strptime(date_time_string, '%Y-%m-%d %H:%M'), [date_time_from_string, date_time_to_string])
        if date_time_from.minute % 30 != 0 or date_time_to.minute % 30 != 0:
            raise ValueError('Both dates must be rounded to full hours or half (:00/:30)')
        if (date_time_to - date_time_from).total_seconds() <= 0:
            raise ValueError('End date must be later than start date')

        weekday_from, weekday_to = map(lambda date_time: self._database['open_hours'][date_time.weekday()], [date_time_from, date_time_to])

        def weekday_timedelta(date_time, weekday_open_close):
            return (datetime.timedelta(hours=date_time.hour, minutes=date_time.minute) - datetime.timedelta(hours=weekday_open_close)).total_seconds()
        if not weekday_from['is_open']\
                or not weekday_to['is_open']\
                or weekday_timedelta(date_time_from, weekday_from['open']) < 0\
                or weekday_timedelta(date_time_from, weekday_from['close']) > 0\
                or weekday_timedelta(date_time_to, weekday_to['open']) < 0 \
                or weekday_timedelta(date_time_to, weekday_to['close']) > 0:
            raise ValueError('Rental shop is closed during this time')

        for reservation in filter(lambda reservation_lambda: reservation_lambda['game'] == game_id, self._database['reservations']):
            reservation_date_from, reservation_date_to = map(lambda from_to: datetime.datetime.strptime(reservation[from_to], '%Y-%m-%d %H:%M'), ['from', 'to'])
            if ((date_time_from - reservation_date_from).total_seconds() >= 0 > (date_time_from - reservation_date_to).total_seconds())\
                    or ((date_time_to - reservation_date_from).total_seconds() > 0 >= (date_time_to - reservation_date_to).total_seconds()):
                raise ValueError('Game is already reserved during this time')

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

    def add_user(self, name, lastname, email):
        if type(name) != str or type(lastname) != str:
            raise TypeError('Names must be strings')
        if name == '' or lastname == '':
            raise ValueError('Names must not be empty')
        new_user_id = str(uuid.uuid4())
        self._database['users'].append(
            {
                'id': new_user_id,
                'email': email,
                'name': {
                    'first': name,
                    'last': lastname
                }
            }
        )
        return new_user_id
