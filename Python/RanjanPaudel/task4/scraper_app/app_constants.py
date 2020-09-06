empty_signin_form = {
    "userFullName": '',
    "username": '',
    "userDOB": '',
    "userPasswordCreate": '',
    "userPasswordConfirm": ''
}

empty_login_form = {
    "username": '',
    "userPassword": ''
}

tab_list = [
    {
        "label": 'Top rated movies',
        "value": 'top_rated_movies'
    },
    {
        "label": 'Top rated TV shows',
        "value": 'top_rated_tv_shows'
    },
    {
        "label": 'Most popular movies',
        "value": 'most_popular_movies'
    },
    {
        "label": 'Most popular TV shows',
        "value": 'most_popular_tv_shows'
    }
]

tab_label_map = {
    "top_rated_movies": 'Top rated movies',
    "top_rated_tv_shows": 'Top rated TV shows',
    "most_popular_movies": 'Most popular movies',
    "most_popular_tv_shows": 'Most popular TV shows'
}

list_table_columns = {
    "top_rated_movies": {
        "image": {
            "label": '',
            "class": ''
        },
        "title": {
            "label": 'Title',
            "class": 'algn-lft'
        },
        "rank": {
            "label": 'Rank',
            "class": 'algn-rht'
        },
        "release_year": {
            "label": 'Release Year',
            "class": 'algn-rht'
        },
        "imdb_rating": {
            "label": 'IMDb Rating',
            "class": 'algn-rht'
        }
    },
    "top_rated_tv_shows": {
        "image": {
            "label": '',
            "class": ''
        },
        "title": {
            "label": 'Title',
            "class": 'algn-lft'
        },
        "rank": {
            "label": 'Rank',
            "class": 'algn-rht'
        },
        "release_year": {
            "label": 'Release Year',
            "class": 'algn-rht'
        },
        "imdb_rating": {
            "label": 'IMDb Rating',
            "class": 'algn-rht'
        }
    },
    "most_popular_movies": {
        "image": {
            "label": '',
            "class": ''
        },
        "title": {
            "label": 'Title',
            "class": 'algn-lft'
        },
        "release_year": {
            "label": 'Release Year',
            "class": 'algn-rht'
        },
        "imdb_rating": {
            "label": 'IMDb Rating',
            "class": 'algn-rht'
        },
        "position": {
            "label": 'Position (From)',
            "class": 'algn-rht',
            "popularity": {
                "INCREASED": 'color-green',
                "DECREASED": 'color-red',
                "NO CHANGE": 'color-orange'
            }
        }
    },
    "most_popular_tv_shows": {
        "image": {
            "label": '',
            "class": ''
        },
        "title": {
            "label": 'Title',
            "class": 'algn-lft'
        },
        "release_year": {
            "label": 'Release Year',
            "class": 'algn-rht'
        },
        "imdb_rating": {
            "label": 'IMDb Rating',
            "class": 'algn-rht'
        },
        "position": {
            "label": 'Position (From)',
            "class": 'algn-rht',
            "popularity": {
                "INCREASED": 'color-green',
                "DECREASED": 'color-red',
                "NO CHANGE": 'color-orange'
            }
        }
    }
}

list_table_column_keys = {
    "top_rated_movies": ['image', 'title', 'rank', 'release_year', 'imdb_rating'],
    "top_rated_tv_shows": ['image', 'title', 'rank', 'release_year', 'imdb_rating'],
    "most_popular_movies": ['image', 'title', 'release_year', 'imdb_rating', 'position'],
    "most_popular_tv_shows": ['image', 'title', 'release_year', 'imdb_rating', 'position']
}

imdb_base_url = "https://www.imdb.com"

search_map = {
    "top_rated_movies": "/chart/top/?ref_=nv_mv_250",
    "most_popular_movies": "/chart/moviemeter/?ref_=nv_mv_mpm",
    "top_rated_tv_shows": "/chart/toptv/?ref_=nv_tvv_250",
    "most_popular_tv_shows": "/chart/tvmeter/?ref_=nv_tvv_mptv"
}
