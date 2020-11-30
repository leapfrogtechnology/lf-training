import re
from bs4 import BeautifulSoup

imdb_base_url = "https://www.imdb.com"

search_map = {
    "top_rated_movies": "/chart/top/?ref_=nv_mv_250",
    "most_popular_movies": "/chart/moviemeter/?ref_=nv_mv_mpm",
    "top_rated_tv_shows": "/chart/toptv/?ref_=nv_tvv_250",
    "most_popular_tv_shows": "/chart/tvmeter/?ref_=nv_tvv_mptv"
}


def get_top_rated_list(table_rows):
    movie_list = []
    for tr in table_rows:
        title_column = tr.find('td', {'class': 'titleColumn'})
        rank_column = tr.find('td', {'class': 'ratingColumn imdbRating'})
        if not (title_column and rank_column):
            return

        title_texts = title_column.get_text(
            separator='_//\\_', strip=True).split('_//\\_')

        rank = title_texts[0].replace('.', '')
        title = title_texts[1]
        year = re.sub(r"^\(|\)$", "", title_texts[2])
        rating_text = rank_column.get_text(strip=True)
        movie_link = title_column.find('a')
        movie_img = tr.find('img', {'alt': f'{title}'})

        movie_list.append({
            "rank": rank,
            "title": title,
            "release_year": year,
            "imdb_rating": rating_text,
            "imdb_link": f"{imdb_base_url}{movie_link['href']}",
            "img_link": movie_img['src']
        })

    return movie_list


def get_most_popular_list(table_rows):
    movie_list = []
    for tr in table_rows:
        title_column = tr.find('td', {'class': 'titleColumn'})
        rank_column = tr.find('td', {'class': 'ratingColumn imdbRating'})
        if not (title_column and rank_column):
            return

        title_texts = title_column.get_text(
            separator='_//\\_', strip=True).replace('\n', '_//\\_').split('_//\\_')

        title = title_texts[0]
        year = re.sub(r"^\(|\)$", "", title_texts[1])
        position = title_texts[2].replace(',', '')
        pre_position = re.sub(
            r"^\(|\)$", "", title_texts[len(title_texts) - 1].strip()).replace(',', '')
        rating_text = rank_column.get_text(strip=True) or 'NOT RATED'
        popularity = ''

        if pre_position == 'no change':
            popularity = pre_position.upper()
            pre_position = position
        elif int(position) < int(pre_position):
            popularity = 'INCREASED'
        else:
            popularity = 'DECREASED'
        movie_link = title_column.find('a')
        movie_img = tr.find('img', {'alt': f'{title}'})

        movie_list.append({
            "title": title,
            "release_year": year,
            "imdb_rating": rating_text,
            "position": position,
            "pre_position": pre_position,
            "popularity": popularity,
            "imdb_link": f"{imdb_base_url}{movie_link['href']}",
            "img_link": movie_img['src']
        })

    return movie_list


def get_movie_list(content, _type):
    soup = BeautifulSoup(content, 'html.parser')

    if not soup:
        raise Exception(f'Could not generate the soup for {_type} list!')

    table_body = soup.find('tbody', {'class': 'lister-list'})
    if not table_body:
        raise Exception(
            f'Listing table not found in given URL: {imdb_base_url + search_map[_type]}.')

    table_rows = table_body.find_all('tr')
    if not table_rows or len(table_rows) < 1:
        raise Exception(f'No table rows found in table lister-list.')

    movie_list = ''
    try:
        if _type == 'top_rated_movies' or _type == 'top_rated_tv_shows':
            movie_list = get_top_rated_list(table_rows)
        elif _type == 'most_popular_movies' or _type == 'most_popular_tv_shows':
            movie_list = get_most_popular_list(table_rows)
    except Exception as error:
        raise Exception(f'Error genarating {_type} list: ', error)

    if not movie_list or len(movie_list) < 1:
        raise Exception(f'Could not prepare list for {_type}!')

    return movie_list
