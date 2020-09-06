from sqlalchemy.exc import DBAPIError
import traceback
import requests
from datetime import datetime

import db_models
import errors
import auth
import scraper
from app_constants import imdb_base_url, search_map


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
        traceback.print_stack()
        raise errors.InternalError(
            key='other', message='Could not sign in now!')


def log_in_user(user_data):
    user = []
    try:
        user = db_models.find_user_by_username(user_data['username'])
    except Exception as error:
        traceback.print_stack()
        raise errors.InternalError(
            key='other', message='Could not log in now!')

    if len(user) != 1:
        raise errors.NotFound(
            key='other', message='Account does not exist!')

    is_password_valid = auth.decrypt_password(
        user[0]['password'], user_data['userPassword'])
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
    except Exception as error:
        traceback.print_stack()
        raise errors.InternalError(
            key='other', message='Could not log in now!')


def log_out_user(user_data):
    try:
        db_models.remove_token(user_data)
    except Exception as error:
        traceback.print_stack()


def get_token_info(cookies, _type):
    if _type in cookies:
        return auth.decode_token(
            cookies[_type], _type)

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
    except Exception as error:
        traceback.print_stack()
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
    except Exception as error:
        traceback.print_stack()
        return 'token_invalid'


def scrape(list_name):
    search_url = imdb_base_url + search_map[list_name]
    try:
        response_content = ''
        with requests.get(url=search_url) as req:
            response_content = req.content

        movie_list = scraper.get_movie_list(response_content, list_name)
        db_models.update_movie_list(list_name, movie_list)
        db_models.update_movie_meta(list_name)
    except Exception as error:
        raise Exception


def get_scraped_list(list_name):
    try:
        movie_list = db_models.find_all_movies(list_name),
        movie_meta = db_models.find_movie_meta(list_name)
        return {
            "movie_list": movie_list[0],
            "last_updated": datetime.isoformat(movie_meta['last_updated'])
        }
    except Exception as error:
        print(f'Error fetching {list_name} from DB')
        traceback.print_stack()
        return {
            "movie_list": [],
            "last_updated": ''
        }


def map_to_users_db_model(user_data):
    return {
        "full_name": user_data['userFullName'],
        "username": user_data['username'],
        "dob": user_data['userDOB'],
        "password": auth.encrypt_password(user_data['userPasswordConfirm'])
    }


def map_db_to_user(user_data):  # To exclude password
    return {
        "full_name": user_data['full_name'],
        "username": user_data['username'],
        "dob": user_data['dob']
    }
