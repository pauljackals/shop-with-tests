import unittest
import json
from src.rental.stats import Stats


class TestStatsUnittest(unittest.TestCase):
    def setUp(self):
        with open('data/database_for_testing.json') as file:
            database = json.loads(file.read())
        self.database_original = database

    def test_get_all_stats(self):
        stats_manual = {
            'users_total': 2,
            'games_total': 4,
            'systems_total': 3,
            'games_total_in_system': [
                {'id': 0, 'value': 2},
                {'id': 1, 'value': 1},
                {'id': 2, 'value': 1}
            ],
            'total_hours_week': 35,
            'games_dates_reserved': [
                {
                    'id': 1,
                    'dates': [
                        {
                            "from": "2020-12-15 13:00",
                            "to": "2020-12-19 14:30"
                        }
                    ]
                }
            ]
        }
        stats = Stats(self.database_original)
        self.assertDictEqual(stats.get_all_stats(), stats_manual)

    def test_get_users_total(self):
        stats = Stats(self.database_original)
        self.assertEqual(stats.get_users_total(), 2)

    def test_get_games_total(self):
        stats = Stats(self.database_original)
        self.assertEqual(stats.get_games_total(), 4)

    def test_get_systems_total(self):
        stats = Stats(self.database_original)
        self.assertEqual(stats.get_systems_total(), 3)

    def test_get_games_total_in_system(self):
        stats = Stats(self.database_original)
        self.assertListEqual(stats.get_games_total_in_system(), [
                {'id': 0, 'value': 2},
                {'id': 1, 'value': 1},
                {'id': 2, 'value': 1}
        ])

    def test_get_total_hours_week(self):
        stats = Stats(self.database_original)
        self.assertEqual(stats.get_total_hours_week(), 35)

    def test_get_games_dates_reserved(self):
        stats = Stats(self.database_original)
        self.assertListEqual(stats.get_games_dates_reserved(), [
                {
                    'id': 1,
                    'dates': [
                        {
                            "from": "2020-12-15 13:00",
                            "to": "2020-12-19 14:30"
                        }
                    ]
                }
            ])

    def tearDown(self):
        self.database_original = None


if __name__ == '__main__':
    unittest.main()
