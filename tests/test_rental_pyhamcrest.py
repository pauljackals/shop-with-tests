import unittest
from hamcrest import *
from rental.rental import Rental


class TestRentalPyHamcrest(unittest.TestCase):
    def setUp(self):
        self.rental = Rental()

    def test_load_database(self):
        assert_that(self.rental.load_database(), equal_to(True))

    def test_load_database_no_file(self):
        assert_that(calling(self.rental.load_database).with_args('test'), raises(FileNotFoundError))

    def test_load_database_wrong_type(self):
        assert_that(calling(self.rental.load_database).with_args(23), raises(TypeError))

    def test_save_database(self):
        assert_that(self.rental.save_database(), equal_to(True))

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
