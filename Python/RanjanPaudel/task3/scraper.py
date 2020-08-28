import re
import time
import datetime
import requests
import argparse
from bs4 import BeautifulSoup
from multiprocessing import Pool

import file_handler as fh
import sqlite_handler as sh
import mysql_handler as myh

imdb_base_url = "https://www.imdb.com"

table_list = [
    "top_rated_movies",
    "most_popular_movies",
    "top_rated_tv_shows",
    "most_popular_tv_shows"
]

search_map = {
    "top_rated_movies": "/chart/top/?ref_=nv_mv_250",
    "most_popular_movies": "/chart/moviemeter/?ref_=nv_mv_mpm",
    "top_rated_tv_shows": "/chart/toptv/?ref_=nv_tvv_250",
    "most_popular_tv_shows": "/chart/tvmeter/?ref_=nv_tvv_mptv"
}

table_map = {
    "top_rated_movies": "top_rated_movies",
    "most_popular_movies": "most_popular_movies",
    "top_rated_tv_shows": "top_rated_tv_shows",
    "most_popular_tv_shows": "most_popular_tv_shows"
}

table_label_map = {
    "top_rated_movies": "Top Rated Movies",
    "most_popular_movies": "Most Popular Movies",
    "top_rated_tv_shows": "Top Rated TV Shows",
    "most_popular_tv_shows": "Most Popular TV Shows"
}

parser = argparse.ArgumentParser(description='Scrape with and without multiprocessing',
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--multi",
                    help='Choose to activate or deactivate multiprocessing',
                    choices=(['on', 'off']),
                    required=True)


def get_top_rated_list(table_rows):
    movie_list = []
    for tr in table_rows:
        title_column = tr.find('td', {'class': 'titleColumn'})
        rank_column = tr.find('td', {'class': 'ratingColumn imdbRating'})

        title_texts = title_column.get_text(
            separator='_//\\_', strip=True).split('_//\\_')

        rank = title_texts[0].replace('.', '')
        title = title_texts[1]
        year = re.sub("^\(|\)$", "", title_texts[2])
        rating_text = rank_column.get_text(strip=True)

        movie_list.append({
            "rank": rank,
            "title": title,
            "release_year": year,
            "imdb_rating": rating_text
        })

    return movie_list


def get_most_popular_list(table_rows):
    movie_list = []
    for tr in table_rows:
        title_column = tr.find('td', {'class': 'titleColumn'})
        rank_column = tr.find('td', {'class': 'ratingColumn imdbRating'})

        title_texts = title_column.get_text(
            separator='_//\\_', strip=True).replace('\n', '_//\\_').split('_//\\_')

        title = title_texts[0]
        year = re.sub("^\(|\)$", "", title_texts[1])
        position = title_texts[2].replace(',', '')
        pre_position = re.sub(
            "^\(|\)$", "", title_texts[len(title_texts) - 1]).replace(',', '')
        rating_text = rank_column.get_text(strip=True) or 'NOT RATED'
        popularity = ''

        if pre_position == 'no change':
            popularity = pre_position.upper()
            pre_position = position
        elif int(position) < int(pre_position):
            popularity = 'INCREASED'
        else:
            popularity = 'DECREASED'

        movie_list.append({
            "title": title,
            "release_year": year,
            "imdb_rating": rating_text,
            "position": position,
            "pre_position": pre_position,
            "popularity": popularity
        })

    return movie_list


def get_movie_list(soup, _type):
    table_body = soup.find('tbody', {'class': 'lister-list'})
    table_rows = table_body.find_all('tr')

    if _type == 'top_rated_movies' or _type == 'top_rated_tv_shows':
        return get_top_rated_list(table_rows)

    if _type == 'most_popular_movies' or _type == 'most_popular_tv_shows':
        return get_most_popular_list(table_rows)


def store_in_files(data_list, list_type):
    print('    ** Writing CSV file...')
    fh.store_in_csv(data_list, f'./{list_type}/file.csv')
    print('    ** Writing JSON file...')
    fh.store_in_json(data_list, f'./{list_type}/file.json')
    print('    ** Writing XML file...')
    fh.store_in_xml(data_list, f'./{list_type}/file.xml')
    print('    ** Writing YAML file...')
    fh.store_in_yaml(data_list, f'./{list_type}/file.yaml')
    print('*** Done.')


def store_in_sqlite(table_name, data_list):
    sh.insert_many(table_name, data_list)


def read_from_sqlite(table_name):
    data = sh.fetch_all(table_name)

    print(data)


def store_in_mysql(table_name, data_list):
    myh.insert_many(table_name, data_list)


def read_from_mysql(table_name):
    data = myh.fetch_all(table_name)

    print(data)


def request_and_get_soup(url):
    response_content = ''

    with requests.get(url=url) as req:
        response_content = req.content

    return BeautifulSoup(response_content, 'html.parser')


def scrape_data(_type):
    print(f'Scraping {table_label_map[_type]}:')
    scrape_url = imdb_base_url + search_map[_type]
    print('*** Fetching list...')
    soup = request_and_get_soup(scrape_url)
    print('*** List fetched')
    movie_list = get_movie_list(soup, _type)
    print('*** Saving to files...')
    store_in_files(movie_list, _type)
    print('*** Storing in SQLite DB...')
    store_in_sqlite(table_map[_type], movie_list)
    print('*** Done.')
    print('*** Storing in MySQL DB...')
    store_in_mysql(table_map[_type], movie_list)
    print('*** Done.')
    # read_from_sqlite(table_map[_type])
    # read_from_mysql(table_map[_type])


def scrape_without_multiprocessing():
    print('\nWithout Multiprocessing')
    start_time = time.time()

    scrape_data('top_rated_movies')
    scrape_data('most_popular_movies')
    scrape_data('top_rated_tv_shows')
    scrape_data('most_popular_tv_shows')

    end_time = time.time()
    print('\nScraping Completed')
    print(
        f'\n*******\nTook {round(end_time - start_time, 4)} seconds without multiprocessing\n')


def scrape_with_multiprocessing():
    print('\nWith Multiprocessing')
    start_time = time.time()

    with Pool() as p:
        p.map(scrape_data, table_list)

    end_time = time.time()
    print('\nScraping Completed')
    print(
        f'\n*******\nTook {round(end_time - start_time, 4)} seconds with multiprocessing\n')


def main(arg_dict):
    if arg_dict['multi'] == 'on':
        scrape_with_multiprocessing()

    if arg_dict['multi'] == 'off':
        scrape_without_multiprocessing()


if __name__ == "__main__":
    opts = parser.parse_args()
    main(opts.__dict__)
