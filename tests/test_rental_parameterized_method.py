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
        ('no_file', 'test', FileNotFoundError),
        ('wrong_type', 23, TypeError),
        ('empty_name', '', ValueError)
    ])
    def test_load_database_error(self, name, path, expected):
        with self.assertRaises(expected):
            self.rental.load_database(path)

    @parameterized.expand([
        ('error_empty_name', 'Test', '', 'something@example.com', ValueError),
        ('error_wrong_name_type', 1, 'Testington', 'something@example.com', TypeError),
        ('error_wrong_email_type', 'Test', 'Testington', None, TypeError),
        ('error_email_invalid', 'Test', 'Testington', 'somethingexample.com', ValueError)
    ])
    def test_load_user(self, name, firstname, lastname, email, error):
        with self.assertRaises(error):
            self.rental.add_user(firstname, lastname, email)

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
