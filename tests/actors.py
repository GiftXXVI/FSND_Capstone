import os
import json
import unittest
from datetime import date
from flask_sqlalchemy import SQLAlchemy
from app import APP
from models import setup_db, Actor
from test_utilities import decode_jwt, prepare_genders, prepare_actors, generate_actor


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
                           "dob": "1956-10-29T00:00:00.511Z", "gender_id": self.seed_gender}

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
                permission = 'get:actors'
                if permission in permissions:
                    print(
                        f'\n has {permission}, return code: {response.status_code}')
                    # test response code
                    self.assertEqual(response.status_code, 200)
                    # test response body
                    self.assertEqual(data['success'], True)
                    self.assertIn('actors', data.keys())
                    self.assertGreaterEqual(len(data['actors']), 1)
                else:
                    print(
                        f'\n no {permission}, return code: {response.status_code}')
                    self.assertEqual(response.status_code, 401)
                    self.assertEqual(data['success'], False)
                    self.assertNotIn('actors', data.keys())

    def test_get_actor(self):
        actor = Actor.query.filter(Actor.id == self.seed_id).one_or_none()
        token = self.token
        response = self.client().get(
            f'/actors/{self.seed_id}', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('actors', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('actors', data.keys())
                self.assertEqual(data['success'], False)
            else:
                if actor is None:
                    self.assertEqual(response.status_code, 404)
                    self.assertNotIn('actors', data.keys())
                    self.assertEqual(data['success'], False)
                else:
                    permissions = self.token_detail['permissions']
                    permission = 'get:actors'
                    if permission in permissions:
                        print(
                            f'\n has {permission}, return code: {response.status_code}')
                        self.assertEqual(response.status_code, 200)
                        self.assertIn('actors', data.keys())
                        self.assertEqual(data['success'], True)
                        self.assertEqual(len(data['actors']), 1)
                    else:
                        print(
                            f'\n no {permission}, return code: {response.status_code}')
                        self.assertEqual(response.status_code, 404)
                        self.assertNotIn('actors', data.keys())
                        self.assertEqual(data['success'], False)

    def test_post_actor(self):
        token = self.token
        actor = self.post_actor
        response = self.client().post(
            '/actors', headers={"Authorization": f"Bearer {token}"}, json=actor)
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('actors', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('actors', data.keys())
                self.assertEqual(data['success'], False)
            else:
                permissions = self.token_detail['permissions']
                permission = 'post:actors'
                if permission in permissions:
                    print(
                        f'\n has {permission}, return code: {response.status_code}')
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('actors', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    print(
                        f'\n no {permission}, return code: {response.status_code}')
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('actors', data.keys())
                    self.assertEqual(data['success'], False)

    def test_patch_actor(self):
        token = self.token
        actor = generate_actor(self.seed_gender)
        actor.name = 'Humphrey Bogart'
        actor.dob = date(1899, 12, 25)
        response = self.client().patch(
            f'/actors/{actor.id}', headers={"Authorization": f"Bearer {token}"}, json=actor.in_format())
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('actors', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('actors', data.keys())
                self.assertEqual(data['success'], False)
            else:
                permissions = self.token_detail['permissions']
                permission = 'patch:actors'
                if permission in permissions:
                    print(
                        f'\n has {permission}, return code: {response.status_code}')
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('actors', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    print(
                        f'\n no {permission}, return code: {response.status_code}')
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('actors', data.keys())
                    self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        token = self.token
        actor = generate_actor(self.seed_gender)
        response = self.client().delete(
            f'/actors/{actor.id}', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('actors', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('actors', data.keys())
                self.assertEqual(data['success'], False)
            else:
                permissions = self.token_detail['permissions']
                permission = 'delete:actors'
                if permission in permissions:
                    print(
                        f'\n has {permission}, return code: {response.status_code}')
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('actors', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    print(
                        f'\n no {permission}, return code: {response.status_code}')
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('actors', data.keys())
                    self.assertEqual(data['success'], False)
