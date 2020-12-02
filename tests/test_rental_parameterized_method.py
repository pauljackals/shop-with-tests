import unittest
from parameterized import parameterized
import json
from rental.rental import Rental
import uuid


class TestRentalParameterizedMethod(unittest.TestCase):
    def setUp(self):
        with open('data/database_for_testing.json') as file:
            database = json.loads(file.read())
        self.rental = Rental(database)

    @parameterized.expand([
        ('data/database_for_testing.json', True)
    ])
    def test_load_database(self, path, expected):
        self.assertEqual(self.rental.load_database(path), expected)

    @parameterized.expand([
        ('no_file', 'test', FileNotFoundError, "Database doesn't exist"),
        ('wrong_type', 23, TypeError, 'Database file name must be a string'),
        ('empty_name', '', ValueError, 'Database file name must not be empty')
    ])
    def test_load_database_error(self, name, path, expected, message):
        with self.assertRaisesRegex(expected, '^' + message + '$'):
            self.rental.load_database(path)

    @parameterized.expand([
        ('error_empty_name', 'Test', '', 'something@example.com', ValueError, 'Names must not be empty'),
        ('error_wrong_name_type', 1, 'Testington', 'something@example.com', TypeError, 'Names must be strings'),
        ('error_wrong_email_type', 'Test', 'Testington', None, TypeError, 'Email must be a string'),
        ('error_email_invalid', 'Test', 'Testington', 'somethingexample.com', ValueError, 'Email is not valid')
    ])
    def test_load_user(self, name, firstname, lastname, email, error, message):
        with self.assertRaisesRegex(error, '^' + message + '$'):
            self.rental.add_user(firstname, lastname, email)

    @parameterized.expand([
        ('correct', ('8a85f066-bd8d-43df-b471-a6e708471c4c', 1, '2020-12-19 14:30', '2020-12-21 13:00'), uuid.UUID),
        ('from_day_in_month_february_leap', ('8a85f066-bd8d-43df-b471-a6e708471c4c', 1, '2024-02-29 14:30', '2024-12-21 13:00'), uuid.UUID),
        ('to_day_in_month_february_leap', ('8a85f066-bd8d-43df-b471-a6e708471c4c', 1, '2024-02-21 14:30', '2024-02-29 13:00'), uuid.UUID)
    ])
    def test_create_reservation(self, name, data, instance):
        self.assertIsInstance(uuid.UUID(self.rental.create_reservation(*data), version=4), instance)

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
