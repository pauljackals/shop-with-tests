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

    def test_get_user_reservations(self):
        reservations = [
            {
                "id": "4248797f-9a3e-4a52-b3f7-bb72eef51755",
                "user": "2fe45694-eb13-4283-824e-cd6fb179bfcf",
                "game": 1,
                "from": "2020-12-15 13:00",
                "to": "2020-12-19 14:30"
            }
        ]
        self.rental.load_database()
        assert_that(self.rental.get_user_reservations('2fe45694-eb13-4283-824e-cd6fb179bfcf')).contains_only(*reservations)

    def test_get_user_reservations_wrong_type(self):
        assert_that(self.rental.get_user_reservations).raises(TypeError).when_called_with(123)

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
