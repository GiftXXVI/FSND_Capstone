import os
import string
import random
import json
from jose import jwt
from urllib.request import urlopen
from models import setup_db, Gender, Casting, Actor, Movie


def prepare_movies():
    Movie.query.delete()
    seed_movie = Movie(title="The Girl with the Dragon Tattoo",
                       release_date="2011-12-20")
    seed_movie.insert()
    seed_movie.apply()
    seed_movie.refresh()
    id = seed_movie.id
    seed_movie.dispose()
    return True, seed_movie.id


def prepare_genders():
    Gender.query.delete()
    seed_gender = Gender(name="Male")
    seed_gender.insert()
    seed_gender.apply()
    seed_gender.refresh()
    id = seed_gender.id
    seed_gender.dispose()
    return True, id


def generate_movie():
    title = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=20))
    movie = Movie(title=title, release_date="2001-01-01T00:00:00.511Z")
    movie.insert()
    movie.apply()
    movie.refresh()
    return movie


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
