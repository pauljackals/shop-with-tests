import unittest
from hamcrest import *
from rental.rental import Rental
import uuid
import json
import copy


class TestRentalPyHamcrest(unittest.TestCase):
    def setUp(self):
        with open('data/database_for_testing.json') as file:
            database = json.loads(file.read())
        self.database_for_checking = copy.deepcopy(database)
        self.rental = Rental(database)

    def test_load_database(self):
        assert_that(self.rental.load_database('data/database_for_testing.json'), equal_to(True))

    def test_load_database_no_file(self):
        assert_that(calling(self.rental.load_database).with_args('test'), raises(FileNotFoundError, "^Database doesn't exist$"))

    def test_load_database_wrong_type(self):
        assert_that(calling(self.rental.load_database).with_args(23), raises(TypeError, "^Database file name must be a string$"))

    def test_load_database_empty_name(self):
        assert_that(calling(self.rental.load_database).with_args(''), raises(ValueError), "^Database file name must not be empty$")

    def test_save_database(self):
        assert_that(self.rental.save_database(), equal_to(True))

    def test_save_database_file(self):
        self.rental.save_database()
        with open('src/rental/database_copy.json') as file:
            database_copy = json.loads(file.read())
        assert_that(self.database_for_checking, equal_to(database_copy))

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
        assert_that(calling(self.rental.get_user_reservations).with_args(123), raises(TypeError, '^User ID must be a string$'))

    def test_get_user_reservations_empty(self):
        assert_that(calling(self.rental.get_user_reservations).with_args(''), raises(ValueError, '^User ID must not be empty$'))

    def test_get_user_reservations_no_user(self):
        assert_that(calling(self.rental.get_user_reservations).with_args('test'), raises(LookupError, '^No such user$'))

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
            raises(ValueError, '^Wrong date syntax$')
        )

    def test_create_reservation_wrong_date_to_non_digit(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '20d0-12-21 13:00'
            ),
            raises(ValueError, '^Wrong date syntax$')
        )

    def test_create_reservation_wrong_date_from_wrong_day_in_month(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-11-31 14:30',
                '2020-12-21 13:00'
            ),
            raises(ValueError, '^No such day in provided month$')
        )

    def test_create_reservation_wrong_date_to_wrong_day_in_month(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-04-21 14:30',
                '2021-04-31 13:00'
            ),
            raises(ValueError, '^No such day in provided month$')
        )

    def test_create_reservation_wrong_date_from_wrong_day_in_month_february_non_leap(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-02-29 14:30',
                '2021-12-21 13:00'
            ),
            raises(ValueError, '^No such day in provided month$')
        )

    def test_create_reservation_wrong_date_to_wrong_day_in_month_february_non_leap(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-12-21 14:30',
                '2021-02-29 13:00'
            ),
            raises(ValueError, '^No such day in provided month$')
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

    def test_create_reservation_error_date_from_empty(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '',
                '2020-12-21 13:00'
            ),
            raises(ValueError, '^Wrong date syntax$')
        )

    def test_create_reservation_error_date_to_empty(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                ''
            ),
            raises(ValueError, '^Wrong date syntax$')
        )

    def test_create_reservation_wrong_user_type(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                34,
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ),
            raises(TypeError, '^User ID must be a string$')
        )

    def test_create_reservation_no_user(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                'test',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ),
            raises(LookupError, '^No such user$')
        )

    def test_create_reservation_error_wrong_game_type(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                '1',
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ),
            raises(TypeError, '^Game ID must be an integer$')
        )

    def test_create_reservation_error_empty_user(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ),
            raises(ValueError, '^User ID must not be empty$')
        )

    def test_create_reservation_error_no_game(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                999,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ),
            raises(LookupError, '^No such game$')
        )

    def test_create_reservation_minute_error_date_from(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:29',
                '2020-12-21 13:00'
            ),
            raises(ValueError, '^Both dates must be rounded to full hours or half \(:00/:30\)$')
        )

    def test_create_reservation_minute_error_date_to(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:01'
            ),
            raises(ValueError, '^Both dates must be rounded to full hours or half \(:00/:30\)$')
        )

    def test_create_reservation_error_dates_switched(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-21 13:00',
                '2020-12-19 14:30'
            ),
            raises(ValueError, '^End date must be later than start date$')
        )

    def test_create_reservation_error_date_from_closed_day(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-20 14:30',
                '2020-12-22 13:00'
            ),
            raises(ValueError, '^Rental shop is closed during this time$')
        )

    def test_create_reservation_error_date_to_closed_day(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-20 13:00'
            ),
            raises(ValueError, '^Rental shop is closed during this time$')
        )

    def test_create_reservation_error_date_from_open_hours_before(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 08:30',
                '2020-12-19 13:00'
            ),
            raises(ValueError, '^Rental shop is closed during this time$')
        )

    def test_create_reservation_error_date_from_open_hours_after(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 21:00',
                '2020-12-19 13:00'
            ),
            raises(ValueError, '^Rental shop is closed during this time$')
        )

    def test_create_reservation_error_date_to_open_hours_before(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 14:30',
                '2020-12-19 09:00'
            ),
            raises(ValueError, '^Rental shop is closed during this time$')
        )

    def test_create_reservation_error_date_to_open_hours_after(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 14:00',
                '2020-12-19 16:00'
            ),
            raises(ValueError, '^Rental shop is closed during this time$')
        )

    def test_create_reservation_error_date_from_already_taken(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-15 13:30',
                '2020-12-21 15:00'
            ),
            raises(ValueError, '^Game is already reserved during this time$')
        )

    def test_create_reservation_error_date_to_already_taken(self):
        assert_that(
            calling(self.rental.create_reservation).with_args(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-14 13:30',
                '2020-12-16 15:00'
            ),
            raises(ValueError, '^Game is already reserved during this time$')
        )

    def test_add_user(self):
        assert_that(
            uuid.UUID(self.rental.add_user(
                'Test',
                'Testington',
                'something@example.com'
            ), version=4),
            instance_of(uuid.UUID)
        )

    def test_add_user_error_empty_name(self):
        assert_that(
            calling(self.rental.add_user).with_args(
                'Test',
                '',
                'something@example.com'
            ),
            raises(ValueError, '^Names must not be empty$')
        )

    def test_add_user_error_wrong_name_type(self):
        assert_that(
            calling(self.rental.add_user).with_args(
                1,
                'Testington',
                'something@example.com'
            ),
            raises(TypeError, '^Names must be strings$')
        )

    def test_add_user_error_wrong_email_type(self):
        assert_that(
            calling(self.rental.add_user).with_args(
                'Test',
                'Testington',
                None
            ),
            raises(TypeError, '^Email must be a string$')
        )

    def test_add_user_error_email_invalid(self):
        assert_that(
            calling(self.rental.add_user).with_args(
                'Test',
                'Testington',
                'somethingexample.com'
            ),
            raises(ValueError, '^Email is not valid$')
        )

    def tearDown(self):
        self.rental = None
        self.database_for_checking = None


if __name__ == '__main__':
    unittest.main()
