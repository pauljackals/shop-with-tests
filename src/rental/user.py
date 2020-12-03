class User:
    def __init__(self, data):
        self._id = data['id']
        self._email = data['email']
        self._name = data['name']

    def get_all_data(self):
        return {
            'id': self._id,
            'email': self._email,
            'name': self._name
        }

    def get_id(self):
        return self._id

    def get_email(self):
        return self._email

    def get_name_first(self):
        return self._name['first']
