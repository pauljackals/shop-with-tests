from assertpy import assert_that
from parameterized import parameterized
import json
from rental.rental import Rental


@parameterized([
    ('wrong_date_from_non_digit', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '20d0-12-19 14:30',
            '2020-12-21 13:00'
    ), ValueError),
    ('wrong_date_to_non_digit', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:30',
            '20d0-12-21 13:00'
    ), ValueError)
])
def test_create_reservation(name, data, error):
    with open('data/database_for_testing.json') as file:
        database = json.loads(file.read())
    rental = Rental(database)
    assert_that(rental.create_reservation).raises(error).when_called_with(*data)
