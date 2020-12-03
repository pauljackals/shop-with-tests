import unittest
import json
from rental.rental import Rental


class TestRentalParameterizedFile(unittest.TestCase):
    def test_create_reservation_param_file(self):
        with open('data/parameterized_tests.json') as file:
            tests = json.loads(file.read())

        for test in tests:
            with open('data/database_for_testing.json') as file:
                database = json.loads(file.read())
            rental = Rental(database)

            data = test['data']
            error_string = test['error']
            error = None
            if error_string == 'ValueError':
                error = ValueError

            with self.assertRaisesRegex(error, '^' + test['message'] + '$'):
                rental.create_reservation(data['id_user'], data['id_game'], data['date_start'], data['date_end'])


if __name__ == '__main__':
    unittest.main()
