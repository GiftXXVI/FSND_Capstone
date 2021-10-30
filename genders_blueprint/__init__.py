from flask import Blueprint
from models import Gender
from flask import request, abort, jsonify

genders_blueprint = Blueprint('genders_blueprint', __name__)


@genders_blueprint.route('/genders', methods=['GET'])
def get_genders():
    genders = Gender.query.all()
    format_genders = [gender.format() for gender in genders]
    return jsonify({
        'success': True,
        'genders': format_genders
    })


@genders_blueprint.route('/genders/<int:gender_id>', methods=['GET'])
def get_gender(gender_id):
    gender = Gender.query.filter(Gender.id == gender_id).one_or_none()
    if gender is None:
        abort(404)
    else:
        format_genders = [gender.format()]
        return jsonify({
            'success': True,
            'genders': format_genders
        })


@genders_blueprint.route('/genders', methods=['POST'])
def create_gender():
    success = True
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        name = body.get('name', None)
        if name is None:
            abort(400)
        else:
            gender = Gender(name=name)
            try:
                gender.insert()
                gender.apply()
                gender.refresh()
                format_genders = [gender.format()]
            except:
                gender.rollback()
                success = False
            finally:
                gender.dispose()
                return jsonify({
                    'success': success,
                    'created': gender.id,
                    'genders': format_genders
                })


@genders_blueprint.route('/genders/<int:gender_id>', methods=['PATCH'])
def modify_gender(gender_id):
    success = True
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        name = body.get('name', None)
        if name is None:
            abort(400)
        else:
            gender = Gender.query.filter(Gender.id == gender_id).one_or_none()
            if gender is None:
                abort(422)
            else:
                try:
                    gender.name = name
                    gender.apply()
                    format_genders = [gender.format()]
                except:
                    gender.rollback()
                    success = False
                finally:
                    gender.dispose()
                    if success:
                        return jsonify({
                            'success': success,
                            'modified': gender_id,
                            'genders': format_genders
                        })
                    else:
                        abort(422)


@genders_blueprint.route('/genders/<int:gender_id>', methods=['DELETE'])
def delete_gender(gender_id):
    success = True
    if gender_id is None:
        abort(400)
    else:
        gender = Gender.query.filter(Gender.id == gender_id).one_or_none()
        if gender is None:
            abort(422)
        else:
            try:
                gender.delete()
                gender.apply()
            except:
                gender.rollback()
                success = False
            finally:
                gender.dispose()
                if success:
                    return jsonify({
                        'success': success,
                        'deleted': gender_id,
                        'genders': []
                    })
                else:
                    abort(422)
