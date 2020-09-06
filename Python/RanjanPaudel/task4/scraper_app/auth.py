from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from jwt import InvalidTokenError
import time
import traceback

import config


def generate_token(user, _type):
    jwt_payload = {
        "id": user['id']
    }

    if _type == 'access_token':
        jwt_payload['exp'] = time.time() + float(config.JWT_ACCESS_TOKEN_LIFE)
    elif _type == 'refresh_token':
        jwt_payload['exp'] = time.time() + float(config.JWT_REFRESH_TOKEN_LIFE)

    try:
        return jwt.encode(payload=jwt_payload,
                          key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    except Exception as error:
        raise Exception


def decode_token(token, _type):
    try:
        token_data = jwt.decode(jwt=token, key=config.JWT_SECRET,
                                algorithms=config.JWT_ALGORITHM, verify=False)
        if time.time() > token_data['exp']:
            return {
                "status": 'token_expired',
                "payload": token_data
            }

        return {
            "status": 'valid',
            "payload": token_data
        }
    except InvalidTokenError as error:
        traceback.print_stack()
        return {
            "status": 'token_invalid'
        }


def encrypt_password(password):
    return generate_password_hash(password, method='sha256', salt_length=10)


def decrypt_password(hashed_password, input_password):
    return check_password_hash(hashed_password, input_password)
