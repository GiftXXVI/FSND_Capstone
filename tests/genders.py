import os
import unittest
import json
from app import APP
from models import setup_db, Gender
from flask_sqlalchemy import SQLAlchemy
from test_utilities import decode_jwt, generate_gender, prepare_genders


class TestGenders(unittest.TestCase):
    def setUp(self):
        self.app = APP
        self.client = self.app.test_client
        setup_db(self.app, test_mode=True)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.app = self.app
            self.db.init_app(self.app)

        # prepare the table, clear records, create seed record
        self.seed_id = prepare_genders()
        self.post_gender = {"name": "Female"}

        self.token = os.getenv('TOKEN') if len(
            os.getenv('TOKEN')) > 0 else None
        self.token_detail = decode_jwt(self.token)

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
                permissions = self.token_detail['permissions']
                if 'get:genders' in permissions:
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('genders', data.keys())
                    self.assertEqual(data['success'], True)
                    self.assertGreaterEqual(len(data['genders']), 1)
                else:
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('genders', data.keys())
                    self.assertEqual(data['success'], False)

    def test_get_gender(self):
        gender = Gender.query.filter(Gender.id == self.seed_id).one_or_none()
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
                if gender is None:
                    self.assertEqual(response.status_code, 404)
                    self.assertNotIn('genders', data.keys())
                    self.assertEqual(data['success'], False)
                else:
                    permissions = self.token_detail['permissions']
                    if 'get:genders' in permissions:
                        self.assertEqual(response.status_code, 200)
                        self.assertIn('genders', data.keys())
                        self.assertEqual(data['success'], True)
                        self.assertEqual(len(data['genders']), 1)
                    else:
                        self.assertEqual(response.status_code, 401)
                        self.assertNotIn('genders', data.keys())
                        self.assertEqual(data['success'], False)

    def test_post_gender(self):
        token = self.token
        gender = self.post_gender
        response = self.client().post(
            '/genders', headers={"Authorization": f"Bearer {token}"}, json=gender)
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
                permissions = self.token_detail['permissions']
                if 'post:genders' in permissions:
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('genders', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('genders', data.keys())
                    self.assertEqual(data['success'], False)

    def test_patch_gender(self):
        token = self.token
        gender = generate_gender()
        gender.name = "F"
        response = self.client().patch(
            f'/genders/{gender.id}', headers={"Authorization": f"Bearer {token}"}, json=gender.format())
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
                permissions = self.token_detail['permissions']
                if 'patch:genders' in permissions:
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('genders', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('genders', data.keys())
                    self.assertEqual(data['success'], False)

    def test_delete_gender(self):
        token = self.token
        gender = generate_gender()
        response = self.client().delete(
            f'/genders/{gender.id}', headers={"Authorization": f"Bearer {token}"})
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
                permissions = self.token_detail['permissions']
                if 'delete:genders' in permissions:
                    self.assertEqual(response.status_code, 200)
                    self.assertIn('genders', data.keys())
                    self.assertEqual(data['success'], True)
                else:
                    self.assertEqual(response.status_code, 401)
                    self.assertNotIn('genders', data.keys())
                    self.assertEqual(data['success'], False)
