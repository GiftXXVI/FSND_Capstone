from flask import Blueprint
from models import db, setup_db, Movie, Actor, Gender, Casting
from flask import Flask, request, abort, jsonify

movies_blueprint = Blueprint('movies_blueprint', __name__)


@movies_blueprint.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    format_movies = [movie.format() for movie in movies]
    return jsonify({
        'success': True,
        'movies': format_movies
    })


@movies_blueprint.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    format_movies = [movie.format()]
    return jsonify({
        'success': True,
        'movies': format_movies
    })


@movies_blueprint.route('/movies', methods=['POST'])
def create_movie():
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)
    movie = Movie(title=title, release_date=release_date)
    movie.insert()
    movie.apply()
    movie.refresh()
    format_movies = [movie.format()]
    return jsonify({
        'success': True,
        'created': movie.id,
        'movies': format_movies
    })


@movies_blueprint.route('/movies/<int:movie_id>', methods=['PATCH'])
def modify_movie(movie_id):
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    movie.title = title
    movie.release_date = release_date
    movie.update()
    movie.apply()
    format_movies = [movie.format()]
    return jsonify({
        'success': True,
        'modified': movie.id,
        'movies': format_movies
    })
