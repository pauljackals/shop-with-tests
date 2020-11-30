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

    def test_load_database_no_file(self):
        with self.assertRaises(FileNotFoundError):
            self.rental.load_database('test')

    def test_load_database_wrong_type(self):
        with self.assertRaises(TypeError):
            self.rental.load_database(23)

    def test_save_database(self):
        self.assertTrue(self.rental.save_database())

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
