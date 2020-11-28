import unittest
from assertpy import assert_that
from rental.rental import Rental


class TestRentalAssertPy(unittest.TestCase):
    def setUp(self):
        self.rental = Rental()

    def test_load_database(self):
        assert_that(self.rental.load_database()).is_true()

    def test_load_database_no_file(self):
        assert_that(self.rental.load_database).raises(FileNotFoundError).when_called_with('test')

    def test_load_database_wrong_type(self):
        assert_that(self.rental.load_database).raises(TypeError).when_called_with(23)

    def test_save_database(self):
        assert_that(self.rental.save_database()).is_true()

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
