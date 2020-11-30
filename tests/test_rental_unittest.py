import unittest
import json
from rental.rental import Rental


class TestRentalUnittest(unittest.TestCase):
    def setUp(self):
        with open('../data/database_for_testing.json') as file:
            database = json.loads(file.read())
        self.rental = Rental(database)

    def test_load_database(self):
        self.assertTrue(self.rental.load_database())

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
