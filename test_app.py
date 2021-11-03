import os
from dotenv import dotenv_values
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import APP
from random import choice
from models import setup_db, Gender, Casting, Actor, Movie

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
        token = os.getenv('TOKEN') if len(os.getenv('TOKEN')) > 0 else None
        response = self.client().get(
            '/movies', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)

        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('movies', data.keys())
        else:
            # test response code
            self.assertEqual(response.status_code, 200)

            # test response body
            self.assertEqual(data['success'], True)
            self.assertIn('movies', data.keys())

    def test_get_movie(self):
        movie = Movie.query.filter(Movie.id == 1).one_or_none()
        token = os.getenv('TOKEN') if len(os.getenv('TOKEN')) > 0 else None
        response = self.client().get(
            '/movies/1', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('movies', data.keys())
        else:
            if movie is None:
                self.assertEqual(response.status_code, 404)
                self.assertNotIn('movies', data.keys())
                self.assertEqual(data['success'], False)
            else:
                self.assertEqual(response.status_code, 200)
                self.assertIn('movies', data.keys())
                self.assertEqual(data['success'], True)                


if __name__ == "__main__":
    unittest.main()
