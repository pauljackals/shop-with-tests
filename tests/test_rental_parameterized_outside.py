import unittest
from parameterized import parameterized
from assertpy import assert_that
from rental.rental import Rental


@parameterized([(None, 1)])
def test_load_database(not_required, min_length):
    db = Rental()
    db.load_database()
    assert_that(len(db.database)).is_greater_than_or_equal_to(min_length)


if __name__ == '__main__':
    unittest.main()
