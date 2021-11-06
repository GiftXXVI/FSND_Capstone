from datetime import datetime, date, timedelta
import os
import string
import random
import json
from jose import jwt
from urllib.request import urlopen
from models import setup_db, Gender, Casting, Actor, Movie


def prepare_movies():
    Casting.query.delete()
    Movie.query.delete()
    seed_movie = Movie(title="The Girl with the Dragon Tattoo",
                       release_date=date(2011, 12, 20))
    seed_movie.insert()
    seed_movie.apply()
    seed_movie.refresh()
    id = seed_movie.id
    seed_movie.dispose()
    return id


def prepare_genders():
    Casting.query.delete()
    Actor.query.delete()
    Gender.query.delete()
    seed_gender = Gender(name="Male")
    seed_gender.insert()
    seed_gender.apply()
    seed_gender.refresh()
    id = seed_gender.id
    seed_gender.dispose()
    return id


def prepare_actors(gender_id):
    Casting.query.delete()
    Actor.query.delete()
    seed_actor = Actor(name="Ernest Borgnine",
                       dob=date(1917, 1, 24), gender_id=gender_id)
    seed_actor.insert()
    seed_actor.apply()
    seed_actor.refresh()
    id = seed_actor.id
    seed_actor.dispose()
    return id


def prepare_castings(actor_id, movie_id):
    Casting.query.delete()
    seed_casting = Casting(actor_id=actor_id, movie_id=movie_id,
                           casting_date=datetime.now(), recast_yn=False)
    seed_casting.insert()
    seed_casting.apply()
    seed_casting.refresh()
    id = seed_casting.id
    seed_casting.dispose()
    return id


def generate_movie():
    title = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=20))
    movie = Movie(title=title, release_date=date(2001, 1, 1))
    movie.insert()
    movie.apply()
    movie.refresh()
    return movie


def generate_gender():
    name = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=5))
    gender = Gender(name=name)
    gender.insert()
    gender.apply()
    gender.refresh()
    return gender


def generate_actor(gender_id):
    name = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=5))
    dob = date(1970, 1, 1) +\
        timedelta(days=random.randint(0, 50)*365)
    actor = Actor(name=name, dob=dob, gender_id=gender_id)
    actor.insert()
    actor.apply()
    actor.refresh()
    return actor


def generate_casting(actor_id, movie_id):
    casting_date = datetime.now()
    recast_yn = False
    casting = Casting(actor_id=actor_id, movie_id=movie_id,
                      casting_date=casting_date, recast_yn=recast_yn)
    casting.insert()
    casting.apply()
    casting.refresh()
    return casting

def decode_jwt(token):
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    API_AUDIENCE = os.getenv("API_AUDIENCE")
    AUTH0_CLIENTID = os.getenv("AUTH0_CLIENTID")
    ALGORITHMS = ["RS256"]
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        return 'no_key'
    else:
        for key in jwks['keys']:
            if key['kid'] == unverified_header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer='https://' + AUTH0_DOMAIN + '/'
                )
                return payload
            except jwt.ExpiredSignatureError:
                return 'expired'
            except jwt.JWTClaimsError:
                return 'incorrect_audience_issuer'
            except Exception:
                return 'parse_error'
        else:
            return 'no_key'
