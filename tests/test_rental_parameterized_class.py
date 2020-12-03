import unittest
from parameterized import parameterized_class
import json
from src.rental.rental import Rental


@parameterized_class(
    ('name', 'data', 'error', 'message'), [
        ('error_dates_switched', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-21 13:00',
            '2020-12-19 14:30'
        ), ValueError, 'End date must be later than start date'),
        ('error_date_from_closed_day', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-20 14:30',
            '2020-12-22 13:00'
        ), ValueError, 'Rental shop is closed during this time'),
        ('error_date_to_closed_day', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:30',
            '2020-12-20 13:00'
        ), ValueError, 'Rental shop is closed during this time'),
        ('error_date_from_open_hours_before', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-18 08:30',
            '2020-12-19 13:00'
        ), ValueError, 'Rental shop is closed during this time'),
        ('error_date_from_open_hours_after', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-18 21:00',
            '2020-12-19 13:00'
        ), ValueError, 'Rental shop is closed during this time'),
        ('error_date_to_open_hours_before', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-18 14:30',
            '2020-12-19 09:00'
        ), ValueError, 'Rental shop is closed during this time'),
        ('error_date_to_open_hours_after', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-18 14:00',
            '2020-12-19 16:00'
        ), ValueError, 'Rental shop is closed during this time'),
        ('error_date_from_already_taken', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-15 13:30',
            '2020-12-21 15:00'
        ), ValueError, 'Game is already reserved during this time'),
        ('error_date_to_already_taken', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-14 13:30',
            '2020-12-16 15:00'
        ), ValueError, 'Game is already reserved during this time')
    ]
)
class TestRentalParameterizedClass(unittest.TestCase):
    def setUp(self):
        with open('data/database_for_testing.json') as file:
            database = json.loads(file.read())
        self.rental = Rental(database)

    def test_create_reservation(self):
        with self.assertRaisesRegex(self.error, '^' + self.message + '$'):
            self.rental.create_reservation(*self.data)

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
