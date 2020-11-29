from sqlalchemy.exc import DBAPIError
import traceback
import requests
from requests import RequestException
from datetime import datetime
from jwt import InvalidTokenError

import scraper_app.db_models as db_models
import scraper_app.errors as errors
import scraper_app.auth as auth
import scraper_app.scraper as scraper
from scraper_app.app_constants import imdb_base_url, search_map


def create_new_user(user_data):
    user_exists = db_models.check_user_existance(
        user_data['username'])

    if user_exists:
        raise errors.BadRequest(
            key='username', message='Account for the user already exists!')

    try:
        new_user = map_to_users_db_model(user_data)
        result = db_models.create_user(new_user)
        return result
    except DBAPIError as error:
        errors.print_traceback(error)
        raise errors.InternalError(
            key='other', message='Could not sign in now!')


def log_in_user(user_data):
    user = []
    try:
        user = db_models.find_user_by_username(user_data['username'])
    except DBAPIError as error:
        errors.print_traceback(error)
        raise errors.InternalError(
            key='other', message='Could not log in now!')

    if len(user) != 1:
        raise errors.NotFound(
            key='other', message='Account does not exist!')

    is_password_valid = auth.decrypt_password(
        user[0]['password'], user_data['password'])
    if not is_password_valid:
        raise errors.BadRequest(
            key='other', message='Username and password do not match')

    try:
        access_token = auth.generate_token(user[0], 'access_token')
        refresh_token = auth.generate_token(user[0], 'refresh_token')

        existing_token = db_models.find_token(user[0])
        if existing_token and len(existing_token) > 0:
            db_models.remove_token(user[0])

        db_models.create_token(user[0], refresh_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    except DBAPIError as db_error:
        errors.print_traceback(db_error)
        raise errors.InternalError(
            key='other', message='Could not log in now!')
    except Exception as error:
        errors.print_traceback(error)
        raise errors.InternalError(
            key='other', message='Could not log in now!')


def log_out_user(user_data):
    try:
        db_models.remove_token(user_data)
    except DBAPIError as error:
        errors.print_traceback(error)


def get_token_info(cookies, _type):
    if _type not in cookies:
        return {
            "status": 'token_invalid'
        }

    try:
        return auth.decode_token(
            cookies[_type], _type)
    except InvalidTokenError as token_error:
        errors.print_traceback(token_error)
        return {
            "status": 'token_invalid'
        }


def authenticate_user(cookies):
    access_token_info = get_token_info(cookies, 'access_token')

    if access_token_info['status'] == 'token_invalid':
        return access_token_info['status']

    try:
        user = db_models.find_user_by_id(access_token_info['payload']['id'])
        if len(user) != 1:
            return 'token_invalid'

        token_status = 'valid'
        if(access_token_info['status'] == 'token_expired'):
            token_status = 'token_expired'

        return {
            "status": token_status,
            "user": user[0]
        }
    except DBAPIError as db_error:
        errors.print_traceback(error)
        return 'token_invalid'


def refresh_tokens(cookies):
    access_token_info = get_token_info(cookies, 'access_token')
    if access_token_info['status'] == 'token_invalid':
        return access_token_info['status']

    refresh_token_info = get_token_info(cookies, 'refresh_token')
    if refresh_token_info['status'] == 'token_invalid':
        return refresh_token_info['status']

    if access_token_info['payload']['id'] != refresh_token_info['payload']['id']:
        return 'token_invalid'

    try:
        user = db_models.find_user_by_id(refresh_token_info['payload']['id'])
        if len(user) != 1:
            return 'token_invalid'

        user_refresh_token = db_models.find_token(user[0])
        if not (len(user_refresh_token) == 1
                and user_refresh_token[0]['refresh_token'] == cookies['refresh_token']):
            return 'token_invalid'

        if refresh_token_info['status'] == 'token_expired':
            db_models.remove_token(user[0])
            return refresh_token_info['status']

        new_refresh_token = auth.generate_token(user[0], 'refresh_token')
        db_models.update_token(
            user[0], cookies['refresh_token'], new_refresh_token)
        new_access_token = auth.generate_token(user[0], 'access_token')

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
    except DBAPIError as db_error:
        errors.print_traceback(db_error)
        return 'token_refresh_error'
    except Exception as error:
        errors.print_traceback(error)
        return 'token_refresh_error'


def scrape(list_name):
    search_url = imdb_base_url + search_map[list_name]
    try:
        response_content = ''
        with requests.get(url=search_url) as req:
            response_content = req.content

        movie_list = scraper.get_movie_list(response_content, list_name)
        db_models.update_movie_list(list_name, movie_list)
        db_models.update_movie_meta(list_name)
    except (RequestException, DBAPIError) as error:
        errors.print_traceback(error)
        raise Exception
    except Exception as other_error:
        errors.print_traceback(other_error)
        raise Exception


def get_scraped_list(list_name):
    try:
        movie_list = db_models.find_all_movies(list_name),
        movie_meta = db_models.find_movie_meta(list_name)
        return {
            "movie_list": movie_list[0],
            "last_updated": datetime.isoformat(movie_meta['last_updated'])
        }
    except DBAPIError as error:
        errors.print_traceback(error)
        return {
            "movie_list": [],
            "last_updated": ''
        }


def map_to_users_db_model(user_data):
    return {
        "full_name": user_data['full_name'],
        "username": user_data['username'],
        "dob": user_data['dob'],
        "password": auth.encrypt_password(user_data['confirm_password'])
    }


def map_db_to_user(user_data):  # To exclude password
    return {
        "full_name": user_data['full_name'],
        "username": user_data['username'],
        "dob": user_data['dob']
    }
