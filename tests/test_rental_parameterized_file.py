import unittest
from rental.rental import Rental
import json


class TestRentalParameterizedFile(unittest.TestCase):
    def setUp(self):
        self.rental = Rental()

    def tests_from_file(self):
        with open('../data/test_data.json') as file:
            tests = json.loads(file.read())
        self.rental.load_database()

        self.assertGreaterEqual(len(self.rental.database), tests['tests_special']['test_load_database']['min_length'])

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
