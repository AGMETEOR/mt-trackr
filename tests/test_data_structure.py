import unittest
import json
from data import Data


class TestClass(unittest.TestCase):
    def setUp(self):
        self.data = Data()
        self.request = {
            "title": "Test Title",
            "department": "Test",
            "detail": "Test",
            "status": "Test urgent"
        }
        self.data.add_to_db(self.request)

    def test_get_all_data(self):
        self.assertEqual(len(self.data.get_all_data()), 1)

    def test_get_single_item(self):
        id = self.data.get_all_data()[0]["id"]
        self.assertIn("title", self.data.get_single_item(id))

    def test_add_to_db(self):
        self.data.add_to_db(self.request)
        self.assertEqual(len(self.data.get_all_data()), 2)

    def test_delete_from_db(self):
        id = self.data.get_all_data()[0]["id"]
        self.data.delete_from_db(id)
        self.assertEqual(len(self.data.get_all_data()), 0)

    def test_update_table(self):
        id = self.data.get_all_data()[0]["id"]
        title = "New Title"
        update = {
            "title": title,
            "department": "Test",
            "detail": "Test",
            "status": "Test urgent"
        }
        self.data.update_table(id, update)
        self.assertEqual(self.data.get_single_item(id)["title"], title)


if __name__ == "__main__":
    unittest.main()
