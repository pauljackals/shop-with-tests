import unittest
import json
from src.rental.rental import Rental
import datetime


class TestRentalParameterizedFile(unittest.TestCase):
    def test_create_reservation_param_file(self):
        with open('data/parameterized_tests.json') as file:
            tests = json.loads(file.read())

        for test in tests:
            with open('data/database_for_testing.json') as file:
                database = json.loads(file.read())
            rental = Rental(database, datetime.datetime(year=2020, month=12, day=2, hour=14, minute=17))

            data = test['data']
            for char in ['(', ')']:
                test['message'] = test['message'].replace(char, '\\'+char)
            error_string = test['error']
            error = None
            for error_check in [ValueError, TypeError, LookupError]:
                if error_check.__name__ == error_string:
                    error = error_check

            with self.assertRaisesRegex(error, '^' + test['message'] + '$'):
                rental.create_reservation(data['id_user'], data['id_game'], data['date_start'], data['date_end'])


if __name__ == '__main__':
    unittest.main()
