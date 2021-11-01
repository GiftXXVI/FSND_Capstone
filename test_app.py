import os
from dotenv import dotenv_values
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import APP
from random import choice
from models import setup_db, Gender, Casting, Actor, Movie

from dotenv import load_dotenv
load_dotenv() 


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)

    def tearDown(self):
        pass

    def test_get_movies(self):
        movies = Movie.query.count()
        token = os.getenv('TOKEN') if len(os.getenv('TOKEN')) > 0 else None
        response = self.client().get(
            '/movies', headers={"Authorization": f"Bearer {token}"})
        print(response.data)
        data = json.loads(response.data)

        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('movies', data.keys())
        else:
            if len(movies) > 0:
                # test response code
                self.assertEqual(response.status_code, 200)

                # test response body
                self.assertEqual(data['success'], True)
                self.assertIn('movies', data.keys())
            else:
                # test response code
                self.assertEqual(response.status_code, 404)

                # test response body
                self.assertEqual(data['success'], False)
                self.assertNotIn('movies', data.keys())
                self.assertEqual(data['message'], 'not found')


if __name__ == "__main__":
    unittest.main()
