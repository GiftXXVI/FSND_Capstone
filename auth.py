import json
from functools import wraps
from jose import jwt
import os
from flask import request, abort
from urllib.request import urlopen

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
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
        abort(401, 'Authorization header is expected.')
    else:
        parts = auth.split()
        if 'None' in parts:
            abort(401, 'Token not found.')
        else:
            if parts[0].lower() != 'bearer':
                abort(401, 'Authorization header must start with "Bearer".')
            elif len(parts) == 1:
                abort(401, 'Token not found.')
            elif len(parts) > 2:
                abort(401, 'Authorization header must be bearer token.')
            token = parts[1]
            return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(401, 'Permissions not included in JWT.')
    if permission not in payload['permissions']:
        abort(401, 'Permission not found.')
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        abort(401, 'Authorization malformed.')
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
                abort(401, 'Token expired.')
            except jwt.JWTClaimsError:
                abort(401, 'Incorrect claims. Please, check the audience and issuer.')
            except Exception:
                abort(401, 'Unable to parse authentication token.')
        else:
            abort(403, 'Unable to find the appropriate key.')


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper
    return requires_auth_decorator
