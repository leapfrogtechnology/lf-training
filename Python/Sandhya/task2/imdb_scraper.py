# Scraping Top 10 most watched movies/series from imdb
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import yaml

URL = 'https://www.imdb.com/what-to-watch/popular/?ref_=hm_watch_pop'

class StoreResult:
    
    def csvFile(all_title_list, all_rating_list):
        df = DataFrame(data={'Title':all_title_list, 'Rating': all_rating_list})
        df.to_csv('output/topmovies.csv', sep=',', index = False)
        print('CSV file saved: topmovies.csv')

    def jsonFile(all_title_list, all_rating_list):
        df = DataFrame(data={'Title':all_title_list, 'Rating': all_rating_list}, columns = ['Title', 'Rating'])
        df.to_json('output/topmovies.json')
        print('Json file saved: topmovies.json')

    def yamlFile(all_title_list, all_rating_list):
        # Converting list to dictionary
        movie_dict = {}
        for title in all_title_list:
            for rating in all_rating_list:
                movie_dict[title] = rating

        with open('output/topmovies.yaml', 'w') as file:
            doc = yaml.dump(movie_dict, file)
        print('Yaml file saved: topmovies.yaml')

class TopMovie():
    
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

    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    results = soup.find(role="tabpanel")
    
    scrape_data = results.find_all('div', class_='ipc-poster-card')

    title_list = TopMovie.get_title(scrape_data)
    rating_list = TopMovie.get_rating(scrape_data)

    StoreResult.csvFile(title_list, rating_list)
    StoreResult.jsonFile(title_list, rating_list)
    StoreResult.yamlFile(title_list, rating_list)

if __name__ == "__main__":
    main()
