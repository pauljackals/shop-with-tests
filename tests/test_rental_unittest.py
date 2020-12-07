import unittest
import json
from src.rental.rental import Rental
from src.rental.stats import Stats
import uuid
import copy
import datetime


class TestRentalUnittest(unittest.TestCase):
    def setUp(self):
        with open('data/database_for_testing.json') as file:
            database = json.loads(file.read())
        self.database_for_checking = copy.deepcopy(database)
        self.rental = Rental(database, datetime.datetime(year=2020, month=12, day=2, hour=14, minute=17))

    def test_load_database(self):
        self.assertTrue(self.rental.load_database('data/database_for_testing.json'))

    def test_load_database_no_file(self):
        with self.assertRaisesRegex(FileNotFoundError, "^Database doesn't exist$"):
            self.rental.load_database('test')

    def test_load_database_wrong_type(self):
        with self.assertRaisesRegex(TypeError, "^Database file name must be a string$"):
            self.rental.load_database(23)

    def test_load_database_empty_name(self):
        with self.assertRaisesRegex(ValueError, "^Database file name must not be empty$"):
            self.rental.load_database('')

    def test_save_database(self):
        self.assertTrue(self.rental.save_database())

    def test_save_database_file(self):
        self.rental.save_database()
        with open('src/rental/database_copy.json') as file:
            database_copy = json.loads(file.read())
        self.assertDictEqual(self.database_for_checking, database_copy)

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
        self.assertListEqual(self.rental.get_user_reservations('2fe45694-eb13-4283-824e-cd6fb179bfcf'), reservations)

    def test_get_user_reservations_wrong_type(self):
        with self.assertRaisesRegex(TypeError, '^User ID must be a string$'):
            self.rental.get_user_reservations(123)

    def test_get_user_reservations_empty(self):
        with self.assertRaisesRegex(ValueError, '^User ID must not be empty$'):
            self.rental.get_user_reservations('')

    def test_get_user_reservations_no_user(self):
        with self.assertRaisesRegex(LookupError, '^No such user$'):
            self.rental.get_user_reservations('test')

    def test_create_reservation(self):
        self.assertIsInstance(
            uuid.UUID(self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            ), version=4), uuid.UUID
        )

    def test_create_reservation_wrong_date_from_non_digit(self):
        with self.assertRaisesRegex(ValueError, '^Wrong date syntax$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '20d0-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_wrong_date_to_non_digit(self):
        with self.assertRaisesRegex(ValueError, '^Wrong date syntax$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '20d0-12-21 13:00'
            )

    def test_create_reservation_wrong_date_from_wrong_day_in_month(self):
        with self.assertRaisesRegex(ValueError, '^No such day in provided month$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-11-31 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_wrong_date_to_wrong_day_in_month(self):
        with self.assertRaisesRegex(ValueError, '^No such day in provided month$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-04-21 14:30',
                '2021-04-31 13:00'
            )

    def test_create_reservation_wrong_date_from_wrong_day_in_month_february_non_leap(self):
        with self.assertRaisesRegex(ValueError, '^No such day in provided month$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-02-29 14:30',
                '2021-12-21 13:00'
            )

    def test_create_reservation_wrong_date_to_wrong_day_in_month_february_non_leap(self):
        with self.assertRaisesRegex(ValueError, '^No such day in provided month$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-02-21 14:30',
                '2021-02-29 13:00'
            )

    def test_create_reservation_from_day_in_month_february_leap(self):
        self.assertIsInstance(
            uuid.UUID(self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2024-02-29 14:30',
                '2024-12-21 13:00'
            ), version=4), uuid.UUID)

    def test_create_reservation_to_day_in_month_february_leap(self):
        self.assertIsInstance(
            uuid.UUID(self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2024-02-21 14:30',
                '2024-02-29 13:00'
            ), version=4), uuid.UUID)

    def test_create_reservation_error_date_from_empty(self):
        with self.assertRaisesRegex(ValueError, '^Wrong date syntax$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '',
                '2020-12-21 13:00'
            )

    def test_create_reservation_error_date_to_empty(self):
        with self.assertRaisesRegex(ValueError, '^Wrong date syntax$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                ''
            )

    def test_create_reservation_wrong_user_type(self):
        with self.assertRaisesRegex(TypeError, '^User ID must be a string$'):
            self.rental.create_reservation(
                34,
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_no_user(self):
        with self.assertRaisesRegex(LookupError, '^No such user$'):
            self.rental.create_reservation(
                'test',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_error_wrong_game_type(self):
        with self.assertRaisesRegex(TypeError, '^Game ID must be an integer$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                '1',
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_error_empty_user(self):
        with self.assertRaisesRegex(ValueError, '^User ID must not be empty$'):
            self.rental.create_reservation(
                '',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_error_no_game(self):
        with self.assertRaisesRegex(LookupError, '^No such game$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                999,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_minute_error_date_from(self):
        with self.assertRaisesRegex(ValueError, '^Both dates must be rounded to full hours or half \\(:00/:30\\)$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:29',
                '2020-12-21 13:00'
            )

    def test_create_reservation_minute_error_date_to(self):
        with self.assertRaisesRegex(ValueError, '^Both dates must be rounded to full hours or half \\(:00/:30\\)$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:01'
            )

    def test_create_reservation_error_dates_switched(self):
        with self.assertRaisesRegex(ValueError, '^End date must be later than start date$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-21 13:00',
                '2020-12-19 14:30'
            )

    def test_create_reservation_error_date_from_closed_day(self):
        with self.assertRaisesRegex(ValueError, '^Rental shop is closed during this time$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-20 14:30',
                '2020-12-22 13:00'
            )

    def test_create_reservation_error_date_to_closed_day(self):
        with self.assertRaisesRegex(ValueError, '^Rental shop is closed during this time$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-20 13:00'
            )

    def test_create_reservation_error_date_from_open_hours_before(self):
        with self.assertRaisesRegex(ValueError, '^Rental shop is closed during this time$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 08:30',
                '2020-12-19 13:00'
            )

    def test_create_reservation_error_date_from_open_hours_after(self):
        with self.assertRaisesRegex(ValueError, '^Rental shop is closed during this time$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 21:00',
                '2020-12-19 13:00'
            )

    def test_create_reservation_error_date_to_open_hours_before(self):
        with self.assertRaisesRegex(ValueError, '^Rental shop is closed during this time$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 14:30',
                '2020-12-19 09:00'
            )

    def test_create_reservation_error_date_to_open_hours_after(self):
        with self.assertRaisesRegex(ValueError, '^Rental shop is closed during this time$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 14:00',
                '2020-12-19 16:00'
            )

    def test_create_reservation_error_date_from_already_taken(self):
        with self.assertRaisesRegex(ValueError, '^Game is already reserved during this time$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-15 13:30',
                '2020-12-21 15:00'
            )

    def test_create_reservation_error_date_to_already_taken(self):
        with self.assertRaisesRegex(ValueError, '^Game is already reserved during this time$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-14 13:30',
                '2020-12-16 15:00'
            )

    def test_create_reservation_wrong_date_before_now(self):
        with self.assertRaisesRegex(ValueError, '^Both dates must not be in the past$'):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-11-28 14:30',
                '2020-12-01 13:00'
            )

    def test_add_user(self):
        self.assertIsInstance(
            uuid.UUID(self.rental.add_user(
                'Test',
                'Testington',
                'something@example.com'
            ), version=4), uuid.UUID)

    def test_add_user_error_empty_name(self):
        with self.assertRaisesRegex(ValueError, '^Names must not be empty$'):
            self.rental.add_user(
                'Test',
                '',
                'something@example.com'
            )

    def test_add_user_error_wrong_name_type(self):
        with self.assertRaisesRegex(TypeError, '^Names must be strings$'):
            self.rental.add_user(
                1,
                'Testington',
                'something@example.com'
            )

    def test_add_user_error_wrong_email_type(self):
        with self.assertRaisesRegex(TypeError, '^Email must be a string$'):
            self.rental.add_user(
                'Test',
                'Testington',
                None
            )

    def test_add_user_error_email_invalid(self):
        with self.assertRaisesRegex(ValueError, '^Email is not valid$'):
            self.rental.add_user(
                'Test',
                'Testington',
                'somethingexample.com'
            )

    def test_get_stats(self):
        self.assertIsInstance(self.rental.get_stats(), Stats)

    def tearDown(self):
        self.rental = None
        self.database_for_checking = None


if __name__ == '__main__':
    unittest.main()
