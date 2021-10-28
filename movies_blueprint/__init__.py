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
    if movie is None:
        abort(404)
    else:
        format_movies = [movie.format()]
        return jsonify({
            'success': True,
            'movies': format_movies
        })


@movies_blueprint.route('/movies', methods=['POST'])
def create_movie():
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        check = title is None or release_date is None
        if check:
            abort(400)
        else:
            movie = Movie(title=title, release_date=release_date)
            try:
                movie.insert()
                movie.apply()
                movie.refresh()
                format_movies = [movie.format()]
                return jsonify({
                    'success': True,
                    'created': movie.id,
                    'movies': format_movies
                })
            except:
                abort(422)


@movies_blueprint.route('/movies/<int:movie_id>', methods=['PATCH'])
def modify_movie(movie_id):
    success = True
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        check = title is None or release_date is None or movie_id is None
        if check:
            abort(400)
        else:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            else:
                try:
                    movie.title = title
                    movie.release_date = release_date
                    movie.update()
                    movie.apply()
                    format_movies = [movie.format()]
                except:
                    movie.rollback()
                    success = False
                finally:
                    movie.dispose()
                    if success:
                        return jsonify({
                            'success': success,
                            'modified': movie_id,
                            'movies': format_movies
                        })
                    else:
                        abort(422)


@movies_blueprint.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    success = True
    if movie_id is None:
        abort(400)
    else:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if(movie is None):
            abort(404)
        else:
            try:
                movie.delete()
                movie.apply()
            except:
                movie.rollback()
                success = False
            finally:
                movie.dispose()
                if success:
                    return jsonify({
                        'success': success,
                        'deleted': movie_id,
                        'movies': []
                    })
                else:
                    abort(422)
