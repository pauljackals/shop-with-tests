import unittest
from assertpy import assert_that
from rental.rental import Rental
import uuid


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

    def test_get_user_reservations_no_user(self):
        self.rental.load_database()
        assert_that(self.rental.get_user_reservations).raises(LookupError).when_called_with('test')

    def test_create_reservation(self):
        self.rental.load_database()
        assert_that(
            uuid.UUID(self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ), version=4)
        ).is_instance_of(uuid.UUID)

    def test_create_reservation_wrong_date_from_non_digit(self):
        assert_that(self.rental.create_reservation).raises(ValueError).when_called_with(
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '20d0-12-19 14:30',
            '2020-12-21 13:00'
        )

    def test_create_reservation_wrong_date_to_non_digit(self):
        assert_that(self.rental.create_reservation).raises(ValueError).when_called_with(
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:30',
            '20d0-12-21 13:00'
        )

    def test_create_reservation_wrong_date_from_wrong_day_in_month(self):
        assert_that(self.rental.create_reservation).raises(ValueError).when_called_with(
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-11-31 14:30',
            '2020-12-21 13:00'
        )

    def test_create_reservation_wrong_date_to_wrong_day_in_month(self):
        assert_that(self.rental.create_reservation).raises(ValueError).when_called_with(
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2021-04-21 14:30',
            '2021-04-31 13:00'
        )

    def test_create_reservation_wrong_date_from_wrong_day_in_month_february_non_leap(self):
        assert_that(self.rental.create_reservation).raises(ValueError).when_called_with(
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2021-02-29 14:30',
            '2021-12-21 13:00'
        )

    def test_create_reservation_wrong_date_to_wrong_day_in_month_february_non_leap(self):
        assert_that(self.rental.create_reservation).raises(ValueError).when_called_with(
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2021-02-21 14:30',
            '2021-02-29 13:00'
        )

    def test_create_reservation_from_day_in_month_february_leap(self):
        self.rental.load_database()
        assert_that(
            uuid.UUID(self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2024-02-29 14:30',
                '2024-12-21 13:00'
            ), version=4)
        ).is_instance_of(uuid.UUID)

    def test_create_reservation_to_day_in_month_february_leap(self):
        self.rental.load_database()
        assert_that(
            uuid.UUID(self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2024-02-21 14:30',
                '2024-02-29 13:00'
            ), version=4)
        ).is_instance_of(uuid.UUID)

    def test_create_reservation_wrong_user_type(self):
        assert_that(self.rental.create_reservation).raises(TypeError).when_called_with(
            34,
            1,
            '2020-12-19 14:30',
            '2020-12-21 13:00'
        )

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
