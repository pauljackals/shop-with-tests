import pytest
from assertpy import assert_that
from parameterized import parameterized
import json
from src.rental.rental import Rental
import datetime


@pytest.mark.skip
@parameterized([
    ('wrong_date_from_non_digit', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '20d0-12-19 14:30',
            '2020-12-21 13:00'
    ), ValueError, 'Wrong date syntax'),
    ('wrong_date_to_non_digit', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:30',
            '20d0-12-21 13:00'
    ), ValueError, 'Wrong date syntax'),
    ('wrong_date_from_wrong_day_in_month', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-11-31 14:30',
            '2020-12-21 13:00'
    ), ValueError, 'No such day in provided month'),
    ('wrong_date_to_wrong_day_in_month', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2021-04-21 14:30',
            '2021-04-31 13:00'
    ), ValueError, 'No such day in provided month'),
    ('wrong_date_from_wrong_day_in_month_february_non_leap', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2021-02-29 14:30',
            '2021-12-21 13:00'
    ), ValueError, 'No such day in provided month'),
    ('wrong_date_to_wrong_day_in_month_february_non_leap', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2021-02-21 14:30',
            '2021-02-29 13:00'
    ), ValueError, 'No such day in provided month'),
    ('error_date_from_empty', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '',
            '2020-12-21 13:00'
    ), ValueError, 'Wrong date syntax'),
    ('error_date_to_empty', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:30',
            ''
    ), ValueError, 'Wrong date syntax'),
    ('wrong_user_type', (
            34,
            1,
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), TypeError, 'User ID must be a string'),
    ('no_user', (
            'test',
            1,
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), LookupError, 'No such user'),
    ('error_wrong_game_type', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            '1',
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), TypeError, 'Game ID must be an integer'),
    ('error_empty_user', (
            '',
            1,
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), ValueError, 'User ID must not be empty'),
    ('error_no_game', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            999,
            '2020-12-19 14:30',
            '2020-12-21 13:00'
    ), LookupError, 'No such game'),
    ('minute_error_date_from', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:29',
            '2020-12-21 13:00'
    ), ValueError, 'Both dates must be rounded to full hours or half (:00/:30)'),
    ('minute_error_date_to', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-12-19 14:30',
            '2020-12-21 13:01'
    ), ValueError, 'Both dates must be rounded to full hours or half (:00/:30)'),
    ('wrong_date_before_now', (
            '8a85f066-bd8d-43df-b471-a6e708471c4c',
            1,
            '2020-11-28 14:30',
            '2020-12-01 13:00'
    ), ValueError, 'Both dates must not be in the past')
])
def test_parameterized_create_reservation(name, data, error, message):
    with open('data/database_for_testing.json') as file:
        database = json.loads(file.read())
    rental = Rental(database, datetime.datetime(year=2020, month=12, day=2, hour=14, minute=17))
    assert_that(rental.create_reservation).raises(error).when_called_with(*data).is_equal_to(message)
