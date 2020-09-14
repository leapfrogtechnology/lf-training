import pytest
from bs4 import BeautifulSoup

from scraper import (
    get_movie_list
)

from test_rc.results import (
    top_rated_movies_list,
    most_popular_movies_list
)


def read_file_and_get_soup(file_name):
    file_str = ''
    with open(file_name, 'r') as file:
        file_str = file.read()

    return BeautifulSoup(file_str, 'html.parser')


top_rated_soup = read_file_and_get_soup('test_rc/top_rated_list_test.html')
most_popular_soup = read_file_and_get_soup(
    'test_rc/most_popular_list_test.html')


def test_get_top_rated_list():
    assert get_movie_list(
        top_rated_soup, 'top_rated_movies') == top_rated_movies_list


def test_get_most_popular_list():
    assert get_movie_list(
        most_popular_soup, 'most_popular_movies') == most_popular_movies_list
