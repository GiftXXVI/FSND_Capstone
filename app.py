import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import actors_blueprint
import movies_blueprint
import models
from models import db, setup_db, Movie, Actor, Gender, Casting


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.register_blueprint(actors_blueprint)
    app.register_blueprint(movies_blueprint)
    CORS(app)
    setup_db(app)
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
def error_404():
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'not found'
    }), 404


@APP.errorhandler(422)
def error_422():
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@APP.errorhandler(400)
def error_400():
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad request'
    }), 400


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)