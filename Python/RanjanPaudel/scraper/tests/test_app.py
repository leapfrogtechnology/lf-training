import os
import sys
import pytest
from bs4 import BeautifulSoup

os.environ['FLASK_ENV'] = 'test'


@pytest.fixture
def client():
    from scraper_app import app

    app.app.config['TESTING'] = True

    with app.app.test_client(use_cookies=True) as client:
        yield client


@pytest.fixture
def authorized_client():
    from scraper_app import app

    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        yield client


def test_empty_path_redirection_to_home(client):
    res = client.get('/')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /home.  If not click the link.'

    print('\n1. App redirects to Home or suggests to click the link "/home" for path "/".')


def test_login_page_when_not_logged_in(client):
    res = client.get('/login')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()

    assert title == 'Scraper - Log In'

    print('\n2. App renders Login page for route "/login" when user is not logged in.')


def test_signin_page_when_not_logged_in(client):
    res = client.get('/signin')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()

    assert title == 'Scraper - Sign In'

    print('\n3. App renders Signin page for route "/signin" when user is not logged in.')


def test_home_page_when_not_logged_in(client):
    res = client.get('/home')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n4. App redirects to Login page or suggests to click the link "/login" for route "/home" if the user is not logged in.')


def test_top_rated_movies_page_when_not_logged_in(client):
    res = client.get('/home/top_rated_movies')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n5. App redirects to Login page or suggests to click the link "/login" for route "/home/top_rated_movies" if the user is not logged in.')


def test_top_rated_tv_shows_page_when_not_logged_in(client):
    res = client.get('/home/top_rated_tv_shows')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n6. App redirects to Login page or suggests to click the link "/login" for route "/home/top_rated_tv_shows" if the user is not logged in.')


def test_most_popular_movies_page_when_not_logged_in(client):
    res = client.get('/home/most_popular_movies')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n7. App redirects to Login page or suggests to click the link "/login" for route "/home/most_popular_movies" if the user is not logged in.')


def test_most_popular_tv_shows_page_when_not_logged_in(client):
    res = client.get('/home/most_popular_tv_shows')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n8. App redirects to Login page or suggests to click the link "/login" for route "/home/most_popular_tv_shows" if the user is not logged in.')


def test_scrape_top_rated_movies_when_not_logged_in(client):
    res = client.get('/scrape/top_rated_movies')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n9. App redirects to Login page or suggests to click the link "/login" when user tries to scrape top_rated_movies if the user is not logged in.')


def test_scrape_top_rated_tv_shows_when_not_logged_in(client):
    res = client.get('/scrape/top_rated_tv_shows')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n10. App redirects to Login page or suggests to click the link "/login" when user tries to scrape top_rated_tv_shows if the user is not logged in.')


def test_scrape_most_popular_movies_when_not_logged_in(client):
    res = client.get('/scrape/most_popular_movies')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n11. App redirects to Login page or suggests to click the link "/login" when user tries to scrape most_popular_movies if the user is not logged in.')


def test_scrape_most_popular_tv_shows_when_not_logged_in(client):
    res = client.get('/scrape/most_popular_tv_shows')

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n12. App redirects to Login page or suggests to click the link "/login" when user tries to scrape most_popular_tv_shows if the user is not logged in.')


def test_logout_when_not_logged_in(client):
    res = client.get('/logout')
    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name='p').get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n13. App redirects to Login page or suggests to click the link "/login" for route "/logout" if the user is not logged in.')


def test_signin(client):
    print('\n14. Signing in:')
    # **************************************************
    res = client.post('/signin', data={
        'full_name': 'T',
        'dob': '2000-03-21',
        'username': 'testuser1',
        'new_password': 'thisistest1',
        'confirm_password': 'thisistest1'
    })

    soup = BeautifulSoup(res.data, 'html.parser')
    full_name_error = soup.find(
        name="span", attrs={'id': 'full_name_error'}).get_text()

    assert res.status_code == 400
    assert full_name_error == 'Full name length should be 3 to 100 characters'

    print('\n\ta) With full_name less than 3 characters responds with code 400 and corresponding error message.')
    del res, soup, full_name_error
    # **************************************************
    res = client.post('/signin', data={
        'full_name': 'Test User1',
        'dob': '2000-03-2a',
        'username': 'testuser1',
        'new_password': 'thisistest1',
        'confirm_password': 'thisistest1'
    })

    soup = BeautifulSoup(res.data, 'html.parser')
    dob_error = soup.find(name="span", attrs={'id': 'dob_error'}).get_text()

    assert res.status_code == 400
    assert dob_error == 'Date format should be YYYY-MM-DD'

    print('\n\tb) With dob not in YYYY-MM-DD format responds with code 400 and corresponding error message.')
    del res, soup, dob_error
    # **************************************************
    res = client.post('/signin', data={
        'full_name': 'Test User1',
        'dob': '2000-03-23',
        'username': 'testuser1',
        'new_password': 'this',
        'confirm_password': 'thisistest1'
    })

    soup = BeautifulSoup(res.data, 'html.parser')
    new_password_error = soup.find(
        name="span", attrs={'id': 'new_password_error'}).get_text()

    assert res.status_code == 400
    assert new_password_error == 'Password length should be at least 8 characters'

    print('\n\tc) With password length less than 8 characters responds with code 400 and corresponding error message.')
    del res, soup, new_password_error
    # **************************************************
    res = client.post('/signin', data={
        'full_name': 'Test User1',
        'dob': '2000-03-23',
        'username': 'testuser1',
        'new_password': 'thisistest1',
        'confirm_password': 'thisistest'
    })

    soup = BeautifulSoup(res.data, 'html.parser')
    confirm_password_error = soup.find(
        name="span", attrs={'id': 'confirm_password_error'}).get_text()

    assert res.status_code == 400
    assert confirm_password_error == 'Passwords do not match'

    print('\n\td) With confirmation password not same as new-password responds with code 400 and corresponding error message.')
    del res, soup, confirm_password_error
    # **************************************************
    res = client.post('/signin', data={
        'full_name': 'Test User1',
        'dob': '2000-03-23',
        'username': 'testuser',
        'new_password': 'thisistest1',
        'confirm_password': 'thisistest1'
    })

    soup = BeautifulSoup(res.data, 'html.parser')
    username_error = soup.find(
        name="span", attrs={'id': 'username_error'}).get_text()

    assert res.status_code == 400
    assert username_error == 'Account for the user already exists!'

    print('\n\te) With username already used responds with code 400 and corresponding error message.')
    del res, soup, username_error
    # **************************************************
    new_username = 'testuser1'
    redirection_text = ''
    title = ''
    while True:
        res = client.post('/signin', data={
            'full_name': 'Test User1',
            'dob': '2000-03-23',
            'username': new_username,
            'new_password': 'thisistest1',
            'confirm_password': 'thisistest1'
        })

        soup = BeautifulSoup(res.data, 'html.parser')
        title = soup.find(name='title').get_text()
        redirection_text = soup.find(name='p')

        if redirection_text and redirection_text.get_text() == 'You should be redirected automatically to target URL: /login.  If not click the link.':
            break

        new_username = input(
            f'\n\t- {new_username} seems to be already used please provide a new username to test user creation: ')

    assert title == 'Redirecting...'
    assert redirection_text.get_text(
    ) == 'You should be redirected automatically to target URL: /login.  If not click the link.'

    print('\n\tf) After successful user creation redirects to login page.')
    del res, soup, title, redirection_text


def test_login(client):
    print('\n15. Logging in:')
    # **************************************************
    res = client.post('/login', data={
        'username': 'testuse',
        'password': 'thisistest'
    })

    soup = BeautifulSoup(res.data, 'html.parser')
    error_message = soup.find(
        name="span", attrs={'id': 'error_message'}).get_text()

    assert res.status_code == 404
    assert error_message == 'Account does not exist!'

    print('\n\ta) With username that is not registered responds with code 404 and corresponding error message.')
    del res, soup, error_message
    # **************************************************
    res = client.post('/login', data={
        'username': 'testuser',
        'password': 'thisistes'
    })

    soup = BeautifulSoup(res.data, 'html.parser')
    error_message = soup.find(
        name="span", attrs={'id': 'error_message'}).get_text()

    assert res.status_code == 400
    assert error_message == 'Username and password do not match'

    print('\n\tb) With wrong password responds with code 400 and corresponding error message.')
    del res, soup, error_message
    # **************************************************
    res = client.post('/login', data={
        'username': 'testuser',
        'password': 'qwertyuiop'
    })

    soup = BeautifulSoup(res.data, 'html.parser')
    title = soup.find(name='title').get_text()
    redirection_text = soup.find(name="p").get_text()

    assert title == 'Redirecting...'
    assert redirection_text == 'You should be redirected automatically to target URL: /home.  If not click the link.'

    print('\n\tc) With matching username and password redirects to home page with the tokens required.')
    del res, soup, redirection_text
