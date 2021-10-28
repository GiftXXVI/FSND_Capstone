from flask import Blueprint
from models import db, setup_db, Movie, Actor, Gender, Casting
from flask import Flask, request, abort, jsonify

actors_blueprint = Blueprint('actors_blueprint', __name__)
