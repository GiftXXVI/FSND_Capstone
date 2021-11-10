import os
import json
import random
import unittest
from datetime import date, datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from app import APP
from models import setup_db, Casting
from test_utilities import decode_jwt, prepare_genders
from test_utilities import prepare_actors, prepare_movies
from test_utilities import prepare_castings, generate_casting


class TestCastings(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        setup_db(self.app, test_mode=True)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)

        # prepare the table, clear records, create seed record
        self.seed_movie = prepare_movies()
        self.seed_gender = prepare_genders()
        self.seed_actor = prepare_actors(self.seed_gender)
        self.seed_id = prepare_castings(self.seed_actor, self.seed_movie)
        now = datetime.now()
        self.post_casting = {"actor_id": self.seed_actor,
                             "movie_id": self.seed_movie,
                             "casting_date": json.dumps(now.isoformat()),
                             "recast_yn": 0}

        self.token = os.getenv('TOKEN') if len(
            os.getenv('TOKEN')) > 0 else None
        self.token_detail = decode_jwt(self.token)

    def test_get_castings(self):
        token = self.token
        response = self.client().get(
            '/castings', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)

        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('castings', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertEqual(data['success'], False)
                self.assertNotIn('castings', data.keys())
            else:
                permissions = self.token_detail['permissions']
                permission = 'get:castings'
                if permission in permissions:
                    print(
                        f'\n has {permission},',
                        f'return code: {response.status_code}')
                    # test response code
                    self.assertEqual(response.status_code, 200)
                    # test response body
                    self.assertEqual(data['success'], True)
                    self.assertIn('castings', data.keys())
                    self.assertGreaterEqual(len(data['castings']), 1)
                else:
                    print(
                        f'\n no {permission},',
                        f'return code: {response.status_code}')
                    self.assertEqual(response.status_code, 401)
                    self.assertEqual(data['success'], False)
                    self.assertNotIn('castings', data.keys())

    def test_get_casting(self):
        casting = Casting.query.filter(
            Casting.id == self.seed_id).one_or_none()
        token = self.token
        response = self.client().get(
            f'/castings/{self.seed_id}',
            headers={
                "Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('castings', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('castings', data.keys())
                self.assertEqual(data['success'], False)
            else:
                if casting is None:
                    self.assertEqual(response.status_code, 404)
                    self.assertNotIn('castings', data.keys())
                    self.assertEqual(data['success'], False)
                else:
                    permissions = self.token_detail['permissions']
                    permission = 'get:castings'
                    if permission in permissions:
                        print(
                            f'\n has {permission},',
                            f'return code: {response.status_code}')
                        self.assertEqual(response.status_code, 200)
                        self.assertIn('castings', data.keys())
                        self.assertEqual(data['success'], True)
                        self.assertEqual(len(data['castings']), 1)
                    else:
                        print(
                            f'\n no {permission},',
                            f'return code: {response.status_code}')
                        self.assertEqual(response.status_code, 404)
                        self.assertNotIn('castings', data.keys())
                        self.assertEqual(data['success'], False)

    def test_post_casting(self):
        token = self.token
        casting = self.post_casting
        response = self.client().post(
            '/castings',
            headers={
                "Authorization": f"Bearer {token}"},
            json=casting)
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('castings', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('castings', data.keys())
                self.assertEqual(data['success'], False)
            else:
                permissions = self.token_detail['permissions']
                permission = 'post:castings'
                if permission in permissions:
                    print(
                        f'\n has {permission},',
                        f'return code: {response.status_code}')
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('castings', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    print(
                        f'\n no {permission},',
                        f'return code: {response.status_code}')
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('castings', data.keys())
                    self.assertEqual(data['success'], False)

    def test_patch_casting(self):
        token = self.token
        casting = generate_casting(self.seed_actor, self.seed_movie)
        casting.casting_date = date(1970, 1, 1) +\
            timedelta(days=random.randint(25, 50) * 365)
        response = self.client().patch(
            f'/castings/{casting.id}',
            headers={
                "Authorization": f"Bearer {token}"},
            json=casting.in_format())
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('castings', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('castings', data.keys())
                self.assertEqual(data['success'], False)
            else:
                permissions = self.token_detail['permissions']
                permission = 'patch:castings'
                if permission in permissions:
                    print(
                        f'\n has {permission},',
                        f'return code: {response.status_code}')
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('castings', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    print(
                        f'\n no {permission},',
                        f'return code: {response.status_code}')
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('castings', data.keys())
                    self.assertEqual(data['success'], False)

    def test_delete_casting(self):
        token = self.token
        casting = generate_casting(self.seed_actor, self.seed_movie)
        response = self.client().delete(
            f'/castings/{casting.id}',
            headers={
                "Authorization": f"Bearer {token}"})
        data = json.loads(response.data)
        if token is None:
            self.assertEqual(response.status_code, 401)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'token not found.')
            self.assertNotIn('castings', data.keys())
        else:
            if self.token_detail == 'expired':
                self.assertEqual(response.status_code, 401)
                self.assertNotIn('castings', data.keys())
                self.assertEqual(data['success'], False)
            else:
                permissions = self.token_detail['permissions']
                permission = 'delete:castings'
                if permission in permissions:
                    print(
                        f'\n has {permission},',
                        f'return code: {response.status_code}')
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('castings', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    print(
                        f'\n no {permission},',
                        f'return code: {response.status_code}')
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('castings', data.keys())
                    self.assertEqual(data['success'], False)
