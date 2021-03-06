import unittest
from application import create_app
import json
import jwt
import pprint
from dbHandler import DatabaseHandler


class TestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client

        self.request_body = {
            "id": 565,
            "title": "Elevator Maintenance",
            "department": "Accounts",
            "detail": "We need to repair asap",
            "status": "urgent"
        }

        with self.app.test_client() as c:

            self.signres = c.post('/auth/signup/', headers={'Content-Type': 'application/json; charset=utf-8'}, data=json.dumps(
                {"username": "testingme", "password": "iamsecret", "status": "normal"}))
            self.tk_res = c.post('/auth/login/', headers={'Content-Type': 'application/json; charset=utf-8'}, data=json.dumps(
                {"username": "testingme", "password": "iamsecret"}))

            self.data = self.tk_res.get_json()['token']

            self.res = c.post('api/v1/users/requests/', headers={
                              'Authorization': self.data, 'Content-Type': 'application/json; charset=utf-8'}, data=json.dumps(self.request_body))

    def test_signup(self):
        res = self.client().post('auth/signup/', headers={'Content-Type': 'application/json; charset=utf-8'}, data=json.dumps(
            {"username": "   ", "password": "iamsecret", "status": "normal"}))
        res_one = res = self.client().post('auth/signup/', headers={'Content-Type': 'application/json; charset=utf-8'}, data=json.dumps(
            {"username": "testingme", "password": "iamsecret", "status": "normal"}))
        res_two = res = self.client().post('auth/signup/',
                                           headers={'Content-Type': 'application/json; charset=utf-8'}, data=json.dumps({"password": "iamsecret", "status": "normal"}))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_one.status_code, 403)
        self.assertEqual(res_two.status_code, 403)
        self.assertEqual(self.signres.status_code, 201)

    def test_login(self):
        res = self.client().post('/auth/login/',
                                 headers={'Content-Type': 'application/json; charset=utf-8'}, data=json.dumps({"username": "   ", "password": "iamsecret"}))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(self.tk_res.status_code, 200)
        self.assertIn('token', json.loads(self.tk_res.data))

    def test_request_creation(self):
        self.assertEqual(self.res.status_code, 201)
        self.assertIn('title', json.loads(self.res.data))

    def test_get_all_requests(self):
        self.assertEqual(self.res.status_code, 201)
        res = self.client().get('api/v1/users/requests/',
                                headers={'Authorization': self.data, 'Content-Type': 'application/json; charset=utf-8'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('title', json.loads(res.data)['requests'][0])

    def test_get_single_request(self):
        self.assertEqual(self.res.status_code, 201)
        id = json.loads(self.res.data)["id"]
        print(id)

        res = self.client().get('api/v1/users/requests/{}/'.format(id),
                                headers={'Authorization': self.data, 'Content-Type': 'application/json; charset=utf-8'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(json.loads(res.data)['requests']), 1)
        self.assertIn('title', json.loads(res.data)['requests'][0])

    def test_put_request(self):
        self.assertEqual(self.res.status_code, 201)
        id = json.loads(self.res.data)["id"]
        print(id)
        title = json.loads(self.res.data)["title"]
        newObj = json.loads(self.res.data)
        newObj["title"] = title
        res = self.client().put('api/v1/users/requests/{}/'.format(id), headers={'Authorization': self.data,
                                                                                 'Content-Type': 'application/json; charset=utf-8'}, data=json.dumps(newObj))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(self.res.data)["title"], title)

    def tearDown(self):

        db = DatabaseHandler("postgresql://postgres:allan@localhost:5432/mt_trackr_test_db")
        db.reset_table("new_users_db")
        db.reset_table("requests_db")


if __name__ == "__main__":
    unittest.main()
