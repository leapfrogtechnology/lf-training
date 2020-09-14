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
    df.to_csv('output/articles.csv', index=False, encoding='utf-8')

def save_as_json (all_titles, all_authors):
    data = {'titles':all_titles, 'authors':all_authors}
    df = DataFrame(data, columns= ['titles','authors'])
    df.to_json('output/articles.json')

def main():
    all_titles = []
    all_authors = []
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser') 
    all_titles = scrap_page_title(soup)
    all_authors = scrap_page_authors(soup)
    time.sleep(3)
    # NOTE: looping to scrape all pages
    total_pages = get_total_pages(soup)
    # NOTE: page 1 is already fetched so starting from 2
    for pageNumber in range(2, total_pages+1):
        url_with_pagination = URL + '/page/' + str(pageNumber)
        response = requests.get(url_with_pagination)
        soup = BeautifulSoup(response.text, 'html.parser') 
        all_titles = all_titles + scrap_page_title(soup)
        all_authors = all_authors + scrap_page_authors(soup)
        time.sleep(3)

    save_as_csv(all_titles, all_authors)
    save_as_json(all_titles, all_authors)

if __name__ == "__main__":
    main()
    