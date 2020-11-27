import unittest
from hamcrest import *
from rental.rental import Rental


class TestRentalPyHamcrest(unittest.TestCase):
    def setUp(self):
        self.rental = Rental()

    def test_load_database(self):
        self.rental.load_database()
        assert_that(len(self.rental.database), greater_than(0))

    def test_load_database_no_file(self):
        assert_that(calling(self.rental.load_database).with_args('test'), raises(FileNotFoundError))

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
