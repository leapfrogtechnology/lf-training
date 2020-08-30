# Scraping popular, top picks and fan favourite movies/series from imdb
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import yaml
import os

URL = 'https://www.imdb.com/what-to-watch/'
categories = ['popular','top-picks','fan-favorites']

class StoreResult:
    
    def csvFile(category, all_title_list, all_rating_list):
        filename = os.path.join('output', category) + '.csv'
        df = DataFrame(data={'Title':all_title_list, 'Rating': all_rating_list})
        df.to_csv(filename, sep=',', index = False)
        print('CSV file saved:',filename)

    def jsonFile(category, all_title_list, all_rating_list):
        filename = os.path.join('output', category) + '.json'
        df = DataFrame(data={'Title':all_title_list, 'Rating': all_rating_list}, columns = ['Title', 'Rating'])
        df.to_json(filename)
        print('Json file saved:',filename)

    def yamlFile(category, all_title_list, all_rating_list):
        filename = os.path.join('output', category) + '.yaml'
        # Converting list to dictionary
        movie_dict = {}
        for title in all_title_list:
            for rating in all_rating_list:
                movie_dict[title] = rating

        with open(filename, 'w') as file:
            doc = yaml.dump(movie_dict, file)
        print('Yaml file saved:',filename)

class GetMovieRating():
    
    def get_title(scrape_data):
        title_list = []
        for titles in scrape_data:
            title = titles.find('a', class_='ipc-poster-card__title')
            title_list.append(title.text)
            if None in (title):
                continue
        return title_list

    def get_rating(scrape_data):
        rating_list = []
        for ratings in scrape_data:
            rating = ratings.find('div', class_='ipc-poster-card__rating-star-group')
            rating_list.append(rating.text)
            if None in (rating):
                continue
        return rating_list

def main():

    for category in categories:
        page = requests.get(URL + category)
        soup = BeautifulSoup(page.text, 'html.parser')
        results = soup.find(role = "tabpanel")
        
        scrape_data = results.find_all('div', class_='ipc-poster-card')

        title_list = GetMovieRating.get_title(scrape_data)
        rating_list = GetMovieRating.get_rating(scrape_data)

        StoreResult.csvFile(category, title_list, rating_list)
        StoreResult.jsonFile(category, title_list, rating_list)
        StoreResult.yamlFile(category, title_list, rating_list)

if __name__ == "__main__":
    main()
