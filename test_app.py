import os
from dotenv import dotenv_values
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import APP
from random import choice
from auth import verify_decode_jwt
from models import setup_db, Gender, Casting, Actor, Movie
from jose import jwt
from urllib.request import urlopen


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)

        self.get_movie_id = 1
        self.token = os.getenv('TOKEN') if len(
            os.getenv('TOKEN')) > 0 else None
        self.post_movie = {"title": "Blade Runner 2049",
                           "release_date": "2017-10-03T00:00:00.511Z"}
        self.post_invalid_date_movie = {
            "title": "Blade Runner 2049", "release_date": "2017-02-31T00:00:00.511Z"}
        self.post_invalid_movie = {"title": ""}

    def tearDown(self):
        pass

    def test_get_movies(self):
        token = self.token
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
            self.assertIn(response.status_code, [200, 401])

            if response.status_code == 200:
                # test response body
                self.assertEqual(data['success'], True)
                self.assertIn('movies', data.keys())
            else:
                self.assertEqual(data['success'], False)
                self.assertNotIn('movies', data.keys())

    def test_get_movie(self):
        movie = Movie.query.filter(Movie.id == self.get_movie_id).one_or_none()
        token = self.token
        response = self.client().get(
            f'/movies/{self.get_movie_id}', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('movies', data.keys())
        else:
            if movie is None:
                self.assertIn(response.status_code, [404, 401])
                self.assertNotIn('movies', data.keys())
                self.assertEqual(data['success'], False)
            else:
                self.assertIn(response.status_code, [200, 401])
                if response.status_code == 200:
                    self.assertIn('movies', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    self.assertNotIn('movies', data.keys())
                    self.assertEqual(data['success'], False)

    def test_post_movie(self):
        token = self.token
        movie = self.post_movie
        response = self.client().post('/movies', json=movie)
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('movies', data.keys())
        else:
            self.assertIn(response.status_code, [200, 401])
            if response.status_code == 200:
                self.assertIn('movies', data.keys())
                self.assertEqual(data['success'], True)
            else:
                self.assertNotIn('movies', data.keys())
                self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()
