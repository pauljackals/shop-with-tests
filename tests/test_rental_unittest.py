import unittest
import json
from rental.rental import Rental
import uuid


class TestRentalUnittest(unittest.TestCase):
    def setUp(self):
        with open('../data/database_for_testing.json') as file:
            database = json.loads(file.read())
        self.rental = Rental(database)

    def test_load_database(self):
        self.assertTrue(self.rental.load_database())

    def test_load_database_no_file(self):
        with self.assertRaises(FileNotFoundError):
            self.rental.load_database('test')

    def test_load_database_wrong_type(self):
        with self.assertRaises(TypeError):
            self.rental.load_database(23)

    def test_save_database(self):
        self.assertTrue(self.rental.save_database())

    def test_save_database_file(self):
        self.rental.save_database()
        with open('../data/database_for_testing.json') as file:
            database = json.loads(file.read())
        with open('rental/database_copy.json') as file:
            database_copy = json.loads(file.read())
        self.assertDictEqual(database, database_copy)

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
        with self.assertRaises(TypeError):
            self.rental.get_user_reservations(123)

    def test_get_user_reservations_no_user(self):
        with self.assertRaises(LookupError):
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
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '20d0-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_wrong_date_to_non_digit(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '20d0-12-21 13:00'
            )

    def test_create_reservation_wrong_date_from_wrong_day_in_month(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-11-31 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_wrong_date_to_wrong_day_in_month(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-04-21 14:30',
                '2021-04-31 13:00'
            )

    def test_create_reservation_wrong_date_from_wrong_day_in_month_february_non_leap(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2021-02-29 14:30',
                '2021-12-21 13:00'
            )

    def test_create_reservation_wrong_date_to_wrong_day_in_month_february_non_leap(self):
        with self.assertRaises(ValueError):
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

    def test_create_reservation_wrong_user_type(self):
        with self.assertRaises(TypeError):
            self.rental.create_reservation(
                34,
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_no_user(self):
        with self.assertRaises(LookupError):
            self.rental.create_reservation(
                'test',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_error_wrong_game_type(self):
        with self.assertRaises(TypeError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                '1',
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_error_no_game(self):
        with self.assertRaises(LookupError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                999,
                '2020-12-19 14:30',
                '2020-12-21 13:00'
            )

    def test_create_reservation_minute_error_date_from(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:29',
                '2020-12-21 13:00'
            )

    def test_create_reservation_minute_error_date_to(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-21 13:01'
            )

    def test_create_reservation_error_dates_switched(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-21 13:00',
                '2020-12-19 14:30'
            )

    def test_create_reservation_error_date_from_closed_day(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-20 14:30',
                '2020-12-22 13:00'
            )

    def test_create_reservation_error_date_to_closed_day(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-19 14:30',
                '2020-12-20 13:00'
            )

    def test_create_reservation_error_date_from_open_hours_before(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 08:30',
                '2020-12-19 13:00'
            )

    def test_create_reservation_error_date_from_open_hours_after(self):
        with self.assertRaises(ValueError):
            self.rental.create_reservation(
                '8a85f066-bd8d-43df-b471-a6e708471c4c',
                1,
                '2020-12-18 21:00',
                '2020-12-19 13:00'
            )

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
