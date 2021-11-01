import os
from dotenv import dotenv_values
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Headers
from app import create_app
from random import choice
from auth import AuthError, get_token_auth_header
from models import setup_db, Gender, Casting, Actor, Movie

config = {
    **dotenv_values(".env"),
    **os.environ
}


class CapstoneTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        pass

    def test_get_movies(self):

        token = config['TOKEN'] if len(config['TOKEN']) > 0 else None
        response = self.client().get(
            '/movies', headers={"Authorization": f"Bearer {token}"})
        data = json.loads(response.data)

        movies = Movie.query.count()
        if token is None:
            self.assertRaises(AuthError, get_token_auth_header())
            #test response code
            self.assertEqual(response.status_code, 401)
            #test response body
            self.assertEqual(data['success'], False)
        else:
            if movies > 0:
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
