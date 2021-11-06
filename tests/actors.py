import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import APP
from models import setup_db, Gender, Casting, Actor, Movie
from urllib.request import urlopen
from test_utilities import decode_jwt, prepare_genders, prepare_actors


class TestActors(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        setup_db(self.app, test_mode=True)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)

        # prepare the table, clear records, create seed record
        self.seed_gender = prepare_genders()
        self.seed_id = prepare_actors(self.seed_gender)
        self.post_actor = {"name": "Carrie Fisher",
                           "dob": "1956-10-29T00:00:00.511Z", "gender_id": ""}

        self.token = os.getenv('TOKEN') if len(
            os.getenv('TOKEN')) > 0 else None
        self.token_detail = decode_jwt(self.token)

    def test_get_actors(self):
        token = self.token
        response = self.client().get(
            '/actors', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)

        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('actors', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertEqual(data['success'], False)
                self.assertNotIn('actors', data.keys())
            else:
                permissions = self.token_detail['permissions']
                if 'get:actors' in permissions:
                    # test response code
                    self.assertEqual(response.status_code, 200)
                    # test response body
                    self.assertEqual(data['success'], True)
                    self.assertIn('actors', data.keys())
                    self.assertGreaterEqual(len(data['actors']), 1)
                else:
                    self.assertEqual(response.status_code, 401)
                    self.assertEqual(data['success'], False)
                    self.assertNotIn('actors', data.keys())
