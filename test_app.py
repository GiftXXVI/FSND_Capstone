import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import APP
from random import choice
from auth import verify_decode_jwt
from models import setup_db, Gender, Casting, Actor, Movie
from jose import jwt
from urllib.request import urlopen
from test_utilities import decode_jwt, generate_movie, prepare_genders, prepare_movies


class TestMovies(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)

        # prepare the table, clear records, create seed record
        self.setup_success, self.seed_id = prepare_movies()
        self.token = os.getenv('TOKEN') if len(
            os.getenv('TOKEN')) > 0 else None
        self.token_detail = decode_jwt(self.token)
        print(self.token_detail)
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
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertEqual(data['success'], False)
                self.assertNotIn('movies', data.keys())
            else:
                # test response code
                self.assertEqual(response.status_code, 200)
                # test response body
                self.assertEqual(data['success'], True)
                self.assertIn('movies', data.keys())
                self.assertGreaterEqual(len(data['movies']), 1)

    def test_get_movie(self):
        movie = Movie.query.filter(Movie.id == self.seed_id).one_or_none()
        token = self.token
        response = self.client().get(
            f'/movies/{self.seed_id}', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('movies', data.keys())
        else:            
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('movies', data.keys())
                self.assertEqual(data['success'], False)
            else:
                if movie is None:
                    self.assertEqual(response.status_code, 404)
                    self.assertNotIn('movies', data.keys())
                    self.assertEqual(data['success'], False)
                else:
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('movies', data.keys())
                    self.assertEqual(data['success'], True)
                    self.assertEqual(len(data['movies']), 1)

    def test_post_movie(self):
        token = self.token
        movie = self.post_movie
        response = self.client().post(
            '/movies', headers={"Authorization": f"Bearer {token}"}, json=movie)
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('movies', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('movies', data.keys())
                self.assertEqual(data['success'], False)
            else:
                self.assertEqual(response.status_code, 200)
                self.assertIn('movies', data.keys())
                self.assertEqual(data['success'], True)

    def test_patch_movie(self):
        token = self.token
        movie = generate_movie()
        movie.title = 'Terminator 3: Rise of the Machines'
        movie.release_date = '2003-06-30T00:00:00.511Z'
        response = self.client().patch(
            f'/movies/{movie.id}', headers={"Authorization": f"Bearer {token}"}, json=movie.format())
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('movies', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('movies', data.keys())
                self.assertEqual(data['success'], False)
            else:
                self.assertEqual(response.status_code, 200)
                self.assertIn('movies', data.keys())
                self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        token = self.token
        movie = generate_movie()
        response = self.client().delete(
            f'/movies/{movie.id}', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('movies', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('movies', data.keys())
                self.assertEqual(data['success'], False)
            else:
                self.assertEqual(response.status_code, 200)
                self.assertIn('movies', data.keys())
                self.assertEqual(data['success'], True)


class TestGenders(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)

        # prepare the table, clear records, create seed record
        self.setup_success, self.seed_id = prepare_genders()

        self.token = os.getenv('TOKEN') if len(
            os.getenv('TOKEN')) > 0 else None
        self.token_detail = decode_jwt(self.token)
        print(self.token_detail)

    def tearDown(self):
        pass

    def test_get_genders(self):
        token = self.token
        response = self.client().get(
            '/genders', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('genders', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('genders', data.keys())
                self.assertEqual(data['success'], False)
            else:
                self.assertEqual(response.status_code, 200)
                self.assertIn('genders', data.keys())
                self.assertEqual(data['success'], True)

    def test_get_gender(self):
        token = self.token
        response = self.client().get(
            f'/genders/{self.seed_id}', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('genders', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('genders', data.keys())
                self.assertEqual(data['success'], False)
            else:
                print(data['genders'])
                self.assertEqual(response.status_code, 200)
                self.assertIn('genders', data.keys())
                self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()
