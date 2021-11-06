import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import APP
from models import setup_db, Gender, Casting, Actor, Movie
from urllib.request import urlopen
from test_utilities import decode_jwt, generate_gender, generate_movie, prepare_genders, prepare_movies

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
        #self.setup_success, self.seed_id = prepare_genders()
        #self.post_gender = {"name": "Female"}

        self.token = os.getenv('TOKEN') if len(
            os.getenv('TOKEN')) > 0 else None
        self.token_detail = decode_jwt(self.token)