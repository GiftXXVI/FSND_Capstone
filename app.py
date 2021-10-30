import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_cors import CORS
from actors_blueprint import actors_blueprint
from castings_blueprint import castings_blueprint
from genders_blueprint import genders_blueprint
from movies_blueprint import movies_blueprint
import models
from models import setup_db, Movie, Actor, Gender, Casting, get_db

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(actors_blueprint)
    app.register_blueprint(movies_blueprint)
    app.register_blueprint(genders_blueprint)
    app.register_blueprint(castings_blueprint)
    CORS(app)
    setup_db(app)
    db, migrate = get_db()
    return app


APP = create_app()


@APP.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization, true')
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, OPTIONS, PATCH, DELETE, POST')
    return response


@APP.errorhandler(404)
def error_404(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'not found'
    }), 404

@APP.errorhandler(405)
def error_405(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'not found'
    }), 405


@APP.errorhandler(422)
def error_422(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@APP.errorhandler(400)
def error_400(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400

@APP.errorhandler(500)
def error_500(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'server error'
    }), 500


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
