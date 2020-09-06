from flask import Flask, request, Markup, render_template, redirect, url_for, make_response, flash
from jinja2 import Environment, PackageLoader, select_autoescape
from functools import wraps

import config
import validators
import services
from app_constants import (
    empty_signin_form,
    empty_login_form,
    tab_list,
    list_table_columns,
    list_table_column_keys,
    tab_label_map)

app = Flask(__name__)
app.secret_key = bytes(config.SESSION_SECRET, encoding='utf8')


@app.route('/')
def root_page():
    return redirect(url_for('home_page'))


@app.route('/home', methods=['GET'])
@app.route('/home/<tab_name>', methods=['GET'])
def home_page(tab_name=None):
    authentication_info = services.authenticate_user(
        request.cookies.copy().to_dict(flat=True))

    if authentication_info == 'token_invalid':
        return redirect(url_for('login_page'))

    if ('status' in authentication_info) and (
            authentication_info['status'] == 'token_expired'):
        return redirect(url_for('refresh_tokens', tab_name=tab_name))

    if request.method == 'GET':
        scraped_list = ''
        if tab_name:
            scraped_list = services.get_scraped_list(tab_name)
            if ('movie_list' not in scraped_list) or len(scraped_list['movie_list']) < 1:
                flash(
                    f'Could not load the list for {tab_label_map[tab_name]}', 'error')
        return render_template('home.html',
                               user_is_logged_in=True,
                               user=authentication_info['user'],
                               tab_list=tab_list,
                               selected_tab=tab_name,
                               tab_label_map=tab_label_map,
                               list_table_columns=list_table_columns,
                               list_table_column_keys=list_table_column_keys,
                               scraped_list=scraped_list)


@app.route('/scrape/<list_name>', methods=['GET'])
def scrape_list(list_name=None):
    print(list_name)
    if list_name in tab_label_map.keys():
        try:
            services.scrape(list_name)
            flash(
                f'{tab_label_map[list_name]} scraped successfully!', 'success')
        except Exception as error:
            flash(
                f'Could not scrape {tab_label_map[list_name]} due to some internal errors!', 'error')

        return redirect(url_for('home_page', tab_name=list_name))
    else:
        flash(f'Invalid request!', 'error')
        return redirect(url_for('home_page'))


@app.route('/refresh', methods=['GET'])
def refresh_tokens():
    if request.method == 'GET':
        new_tokens_info = services.refresh_tokens(
            request.cookies.copy().to_dict(flat=True))

        if new_tokens_info in ['token_expired', 'token_invalid']:
            refresh_response = make_response(redirect(url_for('login_page')))
            refresh_response.set_cookie('access_token', '',
                                        path='/', httponly=True, max_age=0)
            refresh_response.set_cookie('refresh_token', '',
                                        path='/refresh', httponly=True, max_age=0)

            return refresh_response

        query_params = request.args.copy().to_dict(flat=True)
        tab_name = ''
        if 'tab_name' in query_params:
            tab_name = query_params['tab_name']
        response = make_response(
            redirect(url_for('home_page', tab_name=tab_name)))
        response.set_cookie('access_token', new_tokens_info['access_token'],
                            path='/', httponly=True, max_age=config.COOKIE_LIFE)
        response.set_cookie('refresh_token', new_tokens_info['refresh_token'],
                            path='/refresh', httponly=True, max_age=config.COOKIE_LIFE)

        return response


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    authentication_info = services.authenticate_user(
        request.cookies.copy().to_dict(flat=True))

    if ('status' in authentication_info) and (
            authentication_info['status'] == 'token_expired'):
        return redirect(url_for('refresh_tokens'))

    if 'user' in authentication_info:
        return redirect(url_for('home_page'))

    if request.method == 'GET':
        return render_template('login.html', form_data=empty_login_form)

    if request.method == 'POST':
        validation = validators.validate_login_form(request.form)

        if validation['has_error']:
            return render_template('login.html', form_data=request.form, error=validation['error'])

        try:
            tokens = services.log_in_user(
                request.form.copy().to_dict(flat=True))

            response = make_response(redirect(url_for('home_page')))
            response.set_cookie('access_token', tokens['access_token'],
                                path='/', httponly=True, max_age=config.COOKIE_LIFE)
            response.set_cookie('refresh_token', tokens['refresh_token'],
                                path='/refresh', httponly=True, max_age=config.COOKIE_LIFE)

            return response
        except Exception as error:
            return render_template('login.html', form_data=request.form, error=error.args[0])


@app.route('/signin', methods=['GET', 'POST'])
def signin_page():
    authentication_info = services.authenticate_user(
        request.cookies.copy().to_dict(flat=True))

    if ('status' in authentication_info) and (
            authentication_info['status'] == 'token_expired'):
        return redirect(url_for('refresh_tokens'))

    if 'user' in authentication_info:
        return redirect(url_for('home_page'))

    if request.method == 'GET':
        return render_template('signin.html', form_data=empty_signin_form)

    if request.method == 'POST':
        validation = validators.validate_signin_form(request.form)

        if validation['has_error']:
            return render_template('signin.html', form_data=request.form, error=validation['error'])

        try:
            services.create_new_user(
                request.form.copy().to_dict(flat=True))
            flash('You were signed in successfully!', 'success')

            return redirect(url_for('login_page'))
        except Exception as error:
            return render_template('signin.html', form_data=request.form, error=error.args[0])


@app.route('/logout', methods=['GET'])
def logout_page():
    authentication_info = services.authenticate_user(
        request.cookies.copy().to_dict(flat=True))

    if 'user' in authentication_info:
        services.log_out_user(authentication_info['user'])

    response = make_response(redirect(url_for('login_page')))
    response.set_cookie('access_token', '',
                        path='/', httponly=True, max_age=0)
    response.set_cookie('refresh_token', '',
                        path='/refresh', httponly=True, max_age=0)

    return response
