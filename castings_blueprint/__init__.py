from flask import Blueprint
from models import Casting
from flask import request, abort, jsonify
from auth import requires_auth

castings_blueprint = Blueprint('castings_blueprint', __name__)


@castings_blueprint.route('/castings', methods=['GET'])
@requires_auth(permission='get:castings')
def get_castings():
    castings = Casting.query.all()
    format_castings = [casting.format() for casting in castings]
    return jsonify({
        'success': True,
        "castings": format_castings
    })


@castings_blueprint.route('/castings/<int:casting_id>', methods=['GET'])
@requires_auth(permission='get:castings')
def get_casting(casting_id):
    casting = Casting.query.filter(Casting.id == casting_id).one_or_none()
    if casting is None:
        abort(404)
    else:
        format_castings = [casting.format()]
        return jsonify({
            'success': True,
            'castings': format_castings
        })


@castings_blueprint.route('/castings', methods=['POST'])
@requires_auth(permission='post:castings')
def create_casting():
    success = False
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        actor_id = body.get('actor_id', None)
        movie_id = body.get('movie_id', None)
        casting_date = body.get('casting_date', None)
        recast_yn = body.get('recast_yn', False)
        check = actor_id is None or movie_id is None or casting_date is None
        if check:
            abort(400)
        else:
            casting = Casting(actor_id=actor_id, movie_id=movie_id,
                              casting_date=casting_date, recast_yn=recast_yn)
            try:
                casting.insert()
                casting.apply()
                casting.refresh()
                format_castings = [casting.format()]
                success = True
            finally:
                if success:
                    casting.dispose()
                    return jsonify({
                        'success': success,
                        'created': casting.id,
                        'castings': format_castings
                    })
                else:
                    casting.rollback()
                    casting.dispose()
                    abort(422)


@castings_blueprint.route('/castings/<int:casting_id>', methods=['PATCH'])
@requires_auth(permission='patch:castings')
def modify(casting_id):
    success = False
    format_castings = []
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        actor_id = body.get('actor_id', None)
        movie_id = body.get('movie_id', None)
        casting_date = body.get('casting_date', None)
        recast_yn = body.get('recast_yn', None)
        check = actor_id is None or movie_id is None or casting_date is None
        if check:
            abort(400)
        else:
            casting = Casting.query.filter(
                Casting.id == casting_id).one_or_none()
            if casting is None:
                abort(422)
            else:
                casting.actor_id = actor_id
                casting.movie_id = movie_id
                casting.casting_date = casting_date
                casting.recast_yn = bool(
                    recast_yn) if recast_yn is not None else casting.recast_yn
                try:
                    casting.apply()
                    format_castings = [casting.format()]
                    success = True
                finally:
                    if success:
                        casting.dispose()
                        return jsonify({
                            'success': success,
                            'modified': casting_id,
                            'castings': format_castings
                        })
                    else:
                        casting.rollback()
                        casting.dispose()
                        abort(422)


@castings_blueprint.route('/castings/<int:casting_id>', methods=['DELETE'])
@requires_auth(permission='delete:castings')
def delete_casting(casting_id):
    success = False
    casting = Casting.query.filter(Casting.id == casting_id).one_or_none()
    if casting is None:
        abort(400)
    else:
        try:
            casting.delete()
            casting.apply()
            success = True
        finally:
            casting.dispose()
            if success:
                casting.dispose()
                return jsonify({
                    'success': success,
                    'deleted': casting_id,
                    'castings': []
                })
            else:
                casting.rollback()
                casting.dispose()
                abort(422)
