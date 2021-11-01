import os
from dotenv import dotenv_values
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import Headers
from app import create_app
from random import choice
from models import setup_db, Gender, Casting, Actor, Movie

config = {
    **dotenv_values(".env"),
    **os.environ
}


class CapstoneTestCase(unittest.TestCase):
    def setup(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def test_get_movies(self):
        token = config['TOKEN']
        response = self.client().get(
            '/movies', Headers={"Authentication": f"Bearer {token}"})
        data = json.loads(response.data)

        movies = Movie.query.count()
        if token is None:
            self.assertEqual(response.status_code, 401)
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
