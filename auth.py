import json
from functools import wraps
from jose import jwt
import os
from flask import request
from urllib.request import urlopen

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getnev("API_AUDIENCE")
AUTH0_CLIENTID = os.getenv("AUTH0_CLIENTID")
ALGORITHMS = ["RS256"]


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

    def format(self):
        return {
            'message': self.error,
            'code': self.status_code
        }


def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if auth is None:
        raise AuthError('Authorization header is expected.', 401)
    else:
        parts = auth.split()
        if parts[0].lower() != 'bearer':
            raise AuthError(
                'Authorization header must start with "Bearer".', 401)
        elif len(parts) == 1:
            raise AuthError('Token not found.', 401)
        elif len(parts) > 2:
            raise AuthError('Authorization header must be bearer token.', 401)
        token = parts[1]
        return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError('Permissions not included in JWT.', 403)
    if permission not in payload['permissions']:
        raise AuthError('Permission not found.', 403)
    return True


def verify_decode_jwt(token):
    print(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')

    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError('Authorization malformed.', 401)
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
                raise AuthError('Token expired.', 401)
            except jwt.JWTClaimsError:
                raise AuthError(
                    'Incorrect claims. Please, check the audience and issuer.', 401)
            except Exception:
                raise AuthError('Unable to parse authentication token.', 400)
        else:
            raise AuthError('Unable to find the appropriate key.', 403)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print('*Permission* ',permission)
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator