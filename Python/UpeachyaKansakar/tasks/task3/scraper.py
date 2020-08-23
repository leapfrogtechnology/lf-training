# Scraping using Multiprocessing

import time
import requests
import urllib.request
from pandas import DataFrame 
from bs4 import BeautifulSoup

URL = 'https://www.opencodez.com/category/web-development'

def scrap_page_title(soup_object):
    title_divs = soup_object.findAll('h2',{'class':'title'})
    titles = []
    for title in title_divs:
        titles.append(title.get_text())   
    return titles  

def scrap_page_authors(soup_object):
    author_divs = soup_object.findAll('a',attrs={'rel':'author'})
    authors = []
    for author in author_divs:
        authors.append(author.get_text())
    return authors

def get_total_pages(soup_object):
    pagination_div = soup_object.find('div',{'class':'pagination'})
    return len(pagination_div.findAll('li'))

def save_as_csv (all_titles, all_authors):
    df = DataFrame({'title':all_titles, 'authors':all_authors}) 
    df.to_csv('output/articles.csv', index=False, mode='a', encoding='utf-8')

def generate_url_with_pagination(total_pages):
    url_array = []
    for pageNumber in range(1, total_pages-1):
        url_array.push(URL + '/page/' + str(pageNumber))
    return url_array

def scrap_and_save_records(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser') 
    all_titles = scrap_page_title(soup)
    all_authors = scrap_page_authors(soup)
    save_as_csv(all_titles, all_authors)
    time.sleep(3)

def main():
    scrap_and_save_records(URL)
    


if __name__ == "__main__":
    main()
