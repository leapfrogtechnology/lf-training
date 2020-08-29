import os
import time
import csv
import json
import urllib.parse as up
from functools import reduce
import concurrent.futures 
import itertools

import requests
from bs4 import BeautifulSoup

import utils
import db
from sqlitedb import store_in_sqlite
import file_write

inputfile = 'searchfile.csv'

DARAZ_BASE_URL = "https://www.daraz.com.np/"
DARAZ_SEARCH_URL = f"{DARAZ_BASE_URL}catalog/?q="

def request_and_get_soup(search_url, timeout=3):
    if not search_url.startswith('https'):
        search_url = f"{DARAZ_SEARCH_URL}{search_url}" 
    response = requests.get(search_url, timeout=timeout)
    if not response.ok:
        return None

    return BeautifulSoup(response.text, 'lxml')

def debug_html(html):
    with open('daraz.txt', mode='a') as debug_file:
        debug_file.write(str(html))

def store_to_database(result):
    values = []
    search_terms = [(i,) for i in result.keys()]
    db.store_data('search_term', search_terms)
    for key, contents in result.items():
        for x in contents.keys():
            for data_ in contents[x]:
                data = utils.format_price(data_)
                values.append(utils.build_db_format(data))
    db.store_data('contents',values)

def scrape_product(soup):
    result_set = soup.find_all('script', type='application/ld+json')
    if not result_set and isinstance(result_set, list):
        return None

    searched_result = json.loads(result_set[0].string)

    row = {}
    try:
        row["title"] = soup.find('span', class_="breadcrumb_item_anchor breadcrumb_item_anchor_last").text
        row["price"] = searched_result['offers']['priceCurrency'] + ': ' + str(max(searched_result['offers']['lowPrice'], searched_result['offers']['highPrice']))  
        row["url_link"] = searched_result['url']
        row["image_url"] = searched_result['image']
        row["description"] = 'No Description'
        row["aggregateRating"] = searched_result['aggregateRating']['ratingValue'] if 'aggregateRating' in searched_result else 'N/A'
        row["brand"] = searched_result['brand']['name']
    except KeyError as err:
        print(f'KeyError:***\n{err}')
        raise
    return row 

def search_for_items(soup):
    searched_result = json.loads(soup.find_all('script', type='application/ld+json')[1].string)

    assert "itemListElement" in searched_result
    product_url =[]
    for item in searched_result["itemListElement"]:
        product_url.append(item["url"])
    
    return product_url
        
def get_search_terms_from_file(inputfile):
    print('Reading Search File')
    with open(inputfile, mode='r') as fp:
        csv_reader = csv.DictReader(fp, delimiter=',')
        search_urls = []
        for reader in csv_reader:
            result ={}
            query = reader['SearchTerm']

            #Encode query param string
            query_param = up.quote(query) 
            search_url = DARAZ_SEARCH_URL.replace("?q=", f"?q={query_param}")
            result[query] = search_url
            search_urls.append(result)  
        return search_urls

def write_to_different_formats(result):
    for brand, content in result.items():
        file_write.write_to_csv(brand, content)
        file_write.write_to_yaml(brand, content)
        file_write.write_to_json(brand, content)

def scrape_search_terms(search_urls, timeout):
    products = {}
    for search_term, search_url in search_urls.items():
        print(f"Searching: {search_term}")
        soup = request_and_get_soup(search_url, timeout)

        if not soup:
            return
        
        searched_products_list = search_for_items(soup)
        products[search_term] = searched_products_list 
    return products

def scrape_search_results(products):
    product_contents ={}

    for product, product_urls in products.items():
        print(f"Scraping Product: {product}")
        info = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            result_soups = executor.map(request_and_get_soup, product_urls)
        
        for soup in result_soups:
            if not soup:
                return
            result = scrape_product(soup)
            if not result:
                return None
            info.append(result)
        product_contents[product] = info
    return product_contents

if __name__ == "__main__":
    if not os.path.isfile(inputfile):
        utils.CsvCreator(inputfile, ['SearchTerm'])
        print('Input Your Search Terms for Daraz')
    
    search_urls = get_search_terms_from_file(inputfile)
    print('Generated Search Url')
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        print('Getting Search Results')
        product_result = executor.map(scrape_search_terms, search_urls, itertools.repeat(2)) #map requires iterable. making a parameter behave like iterable
    
    futures = []
    print('Scraping Products')
    for product in product_result:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures.append(executor.submit(scrape_search_results,product))
    print('Finished Scraping The Products')
    result = {}
    no_result_set = []
    for future in concurrent.futures.as_completed(futures):
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                db.create_table() #Initializes Connection To database once successful Network connection 
                product_contents = future.result()
                for product, contents in product_contents.items():
                    if not contents:
                        no_result_set.append(product)
                        continue #In no result donot append in the result
                    get_result = reduce(utils.flatten_brand_as_key,contents, {})
                    result[product] = get_result
        except requests.ConnectTimeout:
            print("ConnectTimeout.")

    file_write.write_empty_result_sets(no_result_set)
    file_write.write_overall_result(product_contents)
    write_to_different_formats(result)
    store_to_database(result)
    store_in_sqlite()
