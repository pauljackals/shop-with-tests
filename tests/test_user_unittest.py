import unittest
from rental.user import User


class TestUserUnittest(unittest.TestCase):
    def setUp(self):
        data = {
          "id": "8a85f066-bd8d-43df-b471-a6e708471c4c",
          "email": "test@example.com",
          "name": {
            "first": "John",
            "last": "Doe"
          }
        }
        self.user = User(data)
        self.data = data

    def test_get_all_data(self):
        self.assertDictEqual(self.user.get_all_data(), self.data)

    def test_get_id(self):
        self.assertEqual(self.user.get_id(), self.data['id'])

    def test_get_email(self):
        self.assertEqual(self.user.get_email(), self.data['email'])

    def test_get_name_first(self):
        self.assertEqual(self.user.get_name_first(), self.data['name']['first'])

    def test_get_name_last(self):
        self.assertEqual(self.user.get_name_first(), self.data['name']['last'])

    def tearDown(self):
        self.user = None
        self.data = None


if __name__ == '__main__':
    unittest.main()
