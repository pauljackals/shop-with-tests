import unittest
from assertpy import assert_that
from rental.rental import Rental


class TestRentalAssertPy(unittest.TestCase):
    def setUp(self):
        self.rental = Rental()

    def test_load_database(self):
        self.rental.load_database()
        assert_that(len(self.rental.database)).is_greater_than(0)

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
