import unittest
from hamcrest import *
from rental.rental import Rental
import uuid
import json


class TestRentalPyHamcrest(unittest.TestCase):
    def setUp(self):
        with open('../tests/database_for_testing.json') as file:
            database = json.loads(file.read())
        self.rental = Rental(database)

    def test_load_database(self):
        assert_that(self.rental.load_database(), equal_to(True))

    def test_load_database_no_file(self):
        assert_that(calling(self.rental.load_database).with_args('test'), raises(FileNotFoundError))

    def test_load_database_wrong_type(self):
        assert_that(calling(self.rental.load_database).with_args(23), raises(TypeError))

    def test_save_database(self):
        assert_that(self.rental.save_database(), equal_to(True))

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
        assert_that(self.rental.get_user_reservations('2fe45694-eb13-4283-824e-cd6fb179bfcf'), contains_inanyorder(*reservations))

    def test_get_user_reservations_wrong_type(self):
        assert_that(calling(self.rental.get_user_reservations).with_args(123), raises(TypeError))

    def test_get_user_reservations_no_user(self):
        assert_that(calling(self.rental.get_user_reservations).with_args('test'), raises(LookupError))

    def test_create_reservation(self):
        assert_that(
            uuid.UUID(self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ), version=4),
            instance_of(uuid.UUID)
        )

    def test_create_reservation_wrong_date_from_non_digit(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '20d0-12-19 14:30',
                '2020-12-21 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_wrong_date_to_non_digit(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '20d0-12-21 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_wrong_date_from_wrong_day_in_month(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-11-31 14:30',
                '2020-12-21 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_wrong_date_to_wrong_day_in_month(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-04-21 14:30',
                '2021-04-31 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_wrong_date_from_wrong_day_in_month_february_non_leap(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-02-29 14:30',
                '2021-12-21 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_wrong_date_to_wrong_day_in_month_february_non_leap(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-12-21 14:30',
                '2021-02-29 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_from_day_in_month_february_leap(self):
        assert_that(
            uuid.UUID(self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2024-02-29 14:30',
                '2024-12-21 13:00'
            ), version=4),
            instance_of(uuid.UUID)
        )

    def test_create_reservation_to_day_in_month_february_leap(self):
        assert_that(
            uuid.UUID(self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2024-02-21 14:30',
                '2024-02-29 13:00'
            ), version=4),
            instance_of(uuid.UUID)
        )

    def test_create_reservation_wrong_user_type(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                34,
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ),
            raises(TypeError)
        )

    def test_create_reservation_no_user(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                'test',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ),
            raises(LookupError)
        )

    def test_create_reservation_minute_error_date_from(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:29',
                '2020-12-21 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_minute_error_date_to(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:01'
            ),
            raises(ValueError)
        )

    def test_create_reservation_error_dates_switched(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-21 13:00',
                '2020-12-19 14:30'
            ),
            raises(ValueError)
        )

    def test_create_reservation_error_date_from_closed_day(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-20 14:30',
                '2020-12-22 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_error_date_to_closed_day(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-20 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_error_date_from_open_hours_before(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 08:30',
                '2020-12-19 13:00'
            ),
            raises(ValueError)
        )

    def test_create_reservation_error_date_from_open_hours_after(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 21:00',
                '2020-12-19 13:00'
            ),
            raises(ValueError)
        )

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
