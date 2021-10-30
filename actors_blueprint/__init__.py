from flask import Blueprint
from models import Actor
from flask import request, abort, jsonify

actors_blueprint = Blueprint('actors_blueprint', __name__)


@actors_blueprint.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    format_actors = [actor.format() for actor in actors]
    return jsonify({
        "success": True,
        "actors": format_actors
    })


@actors_blueprint.route('/actors/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)
    else:
        format_actors = [actor.format()]
        return jsonify({
            "success": True,
            "actors": format_actors
        })


@actors_blueprint.route('/actors', methods=['POST'])
def create_actor():
    success = True
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        name = body.get('name', None)
        dob = body.get('dob', None)
        gender_id = body.get('gender_id', None)
        check = name is None or dob is None or gender_id is None
        if check:
            abort(400)
        else:
            actor = Actor(name=name, dob=dob, gender_id=gender_id)
            try:
                actor.insert()
                actor.apply()
                actor.refresh()
                format_actors = [actor.format()]
            except:
                actor.rollback()
                success = False
            finally:
                actor.dispose()
                if success:
                    return jsonify({
                        "success": success,
                        'created': actor.id,
                        'actors': format_actors
                    })
