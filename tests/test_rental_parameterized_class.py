import unittest
from parameterized import parameterized_class
import json
from rental.rental import Rental


@parameterized_class(
    ('name', 'data', 'error'), [
        ('error_dates_switched', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-21 13:00',
            '2020-12-19 14:30'
        ), ValueError),
        ('error_date_from_closed_day', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-20 14:30',
            '2020-12-22 13:00'
        ), ValueError),
        ('error_date_to_closed_day', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:30',
            '2020-12-20 13:00'
        ), ValueError)
    ]
)
class TestRentalParameterizedClass(unittest.TestCase):
    def setUp(self):
        with open('data/database_for_testing.json') as file:
            database = json.loads(file.read())
        self.rental = Rental(database)

    def test_create_reservation(self):
        with self.assertRaises(self.error):
            self.rental.create_reservation(*self.data)

    def tearDown(self):
        self.rental = None


if __name__ == '__main__':
    unittest.main()
