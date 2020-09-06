# Store users data on first sign-up with the created_at timestamp. Retrieve users data to authorize user.
users = {
    "id": 'INTEGER PRIMARY KEY AUTO INCREMENT',
    "full_name": 'VARCHAR(255) NOT NULL',
    "username": 'VARCHAR(255) UNIQUE NOT NULL',
    "dob": "DATE NOT NULL",
    "password": "VARCHAR(255) __encrypted__ NOT NULL",
    "created_at": "TIMESTAMP DEFAULT NOT NULL"
}

# Store new refresh-token for a user when logged-in. Whenever user requests for pages, check refresh-token for that user to know logged-in state
# if refresh token has not been expired: refresh the access token of user along with refresh token, else remove refresh token and redirect the
# user to log-in again.
# if user logs out intentionally, remove the user's refresh_token.
tokens = {
    "user_id": "INTEGER NOT NULL FOREIGN KEY REFERENCES users.id",
    "refresh_token": "VARCHAR(255)"
}


# Check database, if data for any list is not available then provide user an option to scrape the data and store.
# If data already exists in db the show the list to user and provide an option to update the list.
# But do not allow to delete the data.
top_rated_movies = {  # Similar for top_rated_tv_shows.
    "rank": "INTEGER UNIQUE NOT NULL",
    "title": "VARCHAR(255) NOT NULL",
    "release_year": "VARCHAR(4) NOT NULL",
    "imdb_rating": "FLOAT NOT NULL",
    "image_link": "TEXT",
    "imdb_link": "VARCHAR(255)",
    "unique": "UNIQUE(title, release_year)"
}

most_popular_movies = {  # Similar for most_popular_tv_shows
    "title": "VARCHAR(255) NOT NULL",
    "release_year": "VARCHAR(4) NOT NULL",
    "imdb_rating": "FLOAT",
    "position": "INTEGER NOT NULL",
    "pre_position": "INTEGER NOT NULL",
    "popularity": "ENUM ('INCREASED', 'DECREASED', 'NO CHANGE') NOT NULL",
    "image_link": "TEXT",
    "imdb_link": "VARCHAR(255)",
    "unique": "UNIQUE(title, release_year)"
}
