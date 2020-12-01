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
    ), ValueError),
    ('wrong_date_from_wrong_day_in_month', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-11-31 14:30',
            '2020-12-21 13:00'
    ), ValueError),
    ('wrong_date_to_wrong_day_in_month', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2021-04-21 14:30',
            '2021-04-31 13:00'
    ), ValueError),
    ('wrong_date_from_wrong_day_in_month_february_non_leap', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2021-02-29 14:30',
            '2021-12-21 13:00'
    ), ValueError),
    ('wrong_date_to_wrong_day_in_month_february_non_leap', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2021-02-21 14:30',
            '2021-02-29 13:00'
    ), ValueError),
    ('error_date_from_empty', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '',
            '2020-12-21 13:00'
    ), ValueError),
    ('error_date_to_empty', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:30',
            ''
    ), ValueError),
    ('wrong_user_type', (
            34,
            1,
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), TypeError),
    ('no_user', (
            'test',
            1,
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), LookupError),
    ('error_wrong_game_type', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            '1',
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), TypeError),
    ('error_empty_user', (
            '',
            1,
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), ValueError),
    ('error_no_game', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            999,
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), LookupError),
    ('minute_error_date_from', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:29',
            '2020-12-21 13:00'
    ), ValueError)
])
def test_create_reservation(name, data, error):
    with open('data/database_for_testing.json') as file:
        database = json.loads(file.read())
    rental = Rental(database)
    assert_that(rental.create_reservation).raises(error).when_called_with(*data)
