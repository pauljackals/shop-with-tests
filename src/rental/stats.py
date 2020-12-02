class Stats:
    def __init__(self, database):
        games = database['games']
        systems = database['systems']
        games_dates_reserved = []
        for reservation in database['reservations']:
            game_index = -1
            game_reserved = list(filter(lambda game: game['id'] == reservation['game'], games_dates_reserved))
            if len(game_reserved):
                game_index = games_dates_reserved.index(game_reserved[0])
            if game_index == -1:
                games_dates_reserved.append({
                    'id': reservation['game'],
                    'dates': []
                })
            games_dates_reserved[game_index]['dates'].append(
                {
                    'from': reservation['from'],
                    'to': reservation['to']
                }
            )

        self._users_total = len(database['users'])
        self._games_total = len(games)
        self._systems_total = len(systems)
        self._games_total_in_system = list(map(lambda system: {
            'id': system['id'],
            'value': len(list(filter(lambda game: game['system'] == system['id'], games)))
        }, systems))
        self._total_hours_week = sum(map(lambda day: day['close'] - day['open'],
                                         filter(lambda day_filter: day_filter['is_open'], database['open_hours'])
                                         ))
        self._games_dates_reserved = games_dates_reserved

    def get_users_total(self):
        return self._users_total

    def get_all_stats(self):
        return {
            'users_total': self._users_total,
            'games_total': self._games_total,
            'systems_total': self._systems_total,
            'games_total_in_system': self._games_total_in_system,
            'total_hours_week': self._total_hours_week,
            'games_dates_reserved': self._games_dates_reserved
        }
