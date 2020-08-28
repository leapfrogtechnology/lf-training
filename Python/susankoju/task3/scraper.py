#!/usr/bin/python3
import os
import csv
import json
import yaml
import sqlite3
import argparse
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from db import saveProduct

DEFAULT_MAX = 50
OUTPUT_FOLDER = 'output'
DEFAULT_SEARCH = 'computer'
DEFAULT_FILENAME = 'results'
BASE_URL = 'https://hamrobazaar.com/'
BASE_SEARCH_URL = BASE_URL + 'search.php'


def get_search_result_rows(data, max=DEFAULT_MAX):
    ''' returns result items array '''
    rows = []
    done = 0
    tables = data.find_all('table', attrs={'border':"0", 'width':"100%", 'cellspacing':"0", 'cellpadding':"0"})
    for table in tables:
        if table.find('td', attrs={'bgcolor':'#C6C6D9'}):
            td_data = table.find_all('td', attrs={'bgcolor': '#F2F4F9'})
            if not td_data:
                # Alternating result background color
                td_data = table.find_all('td', attrs={'bgcolor': '#ECF0F6'})
            if td_data:
                rows.append(td_data)
                done += 1
                if done >= max: break

    return rows


def store_data_in_db(json_data, header, filename=DEFAULT_FILENAME):
    ''' Store data in DB '''
    print('\nStoring data in SQLite database...')
    conn = sqlite3.connect(f'{OUTPUT_FOLDER}/{filename}.db')
    fields = ''.join([(lambda head: str(head)+' text,')(head) for head in header])
    with conn as cursor:
        cursor.execute('CREATE TABLE IF NOT EXISTS data({})'.format(fields[:-1]))
        total = len(json_data['data'])
        saved = 0
        for data in json_data['data']:
            values = ''.join([(lambda key: '"'+str(data[key].replace('"',"''"))+'",')(key) for key in data])
            cursor.execute(f'INSERT INTO data values ({values[:-1]})')
            saved += 1
            os.system(f'echo -ne "\r[{saved}/{total}]"')
            for i in range(saved if saved < 50 else 50):
                os.system(f'echo -ne "#"')
        
    conn.close()
    print(f'\nSQLite database file: {OUTPUT_FOLDER}/{filename}.db    Table name: data')

    print(f'\nStoring data to postgreSQL database...')
    saveProduct(json_data['data'])
    print('Completed!')
    

def store_data_in_files(json_data, header, filename=DEFAULT_FILENAME):
    ''' Store data in files(CSV, JSON, YAML, XML) '''
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    with open(f'{OUTPUT_FOLDER}/{filename}.json', 'w') as outputFile:
        print(f'\nStoring data in JSON file... ')
        json.dump(json_data, outputFile, indent=4)
        print(f'Output file: {OUTPUT_FOLDER}/{filename}.json')

    with open(f'{OUTPUT_FOLDER}/{filename}.csv', 'w') as outputFile:
        print(f'\nStoring data in CSV file... ')
        csv_writer = csv.writer(outputFile)
        csv_writer.writerow(header)
        for data in json_data['data']:
            csv_writer.writerow(data.values())
        print(f'Output file: {OUTPUT_FOLDER}/{filename}.csv')

    with open(f'{OUTPUT_FOLDER}/{filename}.yaml', 'w') as outputFile:
        print(f'\nStoring data in YAML file... ')
        yaml.dump(json_data, outputFile)
        print(f'Output file: {OUTPUT_FOLDER}/{filename}.yaml')
    
    print(f'\nStoring data in XML file... ')
    root = ET.Element('Products')
    for product_data in json_data['data']:
        data = ET.SubElement(root, 'data')
        for key in header:
            ET.SubElement(data, key).text = product_data[key]
    tree = ET.ElementTree(root)
    tree.write(f'{OUTPUT_FOLDER}/{filename}.xml')
    print(f'Output file: {OUTPUT_FOLDER}/{filename}.xml')
    

def extract_data(rows):
    print(f'\nExtracting data from {len(rows)} scrapped results')
    data_keys = ['image', 'title', 'link', 'detail', 'seller', 'seller_items', 'date', 'price']
    json_data = {'data': []}
    for row in rows:
        img = row[0].find('img')['src']
        title = row[1].a.text
        link = BASE_URL + row[1].a['href']
        detail = row[1].text
        seller = row[1].find_all('a')[1].text
        seller_items = BASE_URL + row[1].find_all('a')[1]['href']
        date = row[2].text
        price = row[3].text
        data  = {
            data_keys[0]: img,
            data_keys[1]: title,
            data_keys[2]: link,
            data_keys[3]: detail,
            data_keys[4]: seller,
            data_keys[5]: seller_items,
            data_keys[6]: date,
            data_keys[7]: price
        }
        json_data['data'].append(data)
        
    return (json_data, data_keys)


def get_next_page_url(soup):
    ''' Get next page link '''
    anchor =  soup.find('a', href=True, text='Next')
    if not anchor:
        return False

    href = anchor['href']
    return BASE_SEARCH_URL + href
    

def scrap(url, max=DEFAULT_MAX, results_rows=[]):
    print(f'Target URL: {url}')
    done = len(results_rows)
    print(f'Scrap done: {done}/{max}')
    print('Scrapping...')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    raw_page = requests.get(url, headers=headers)
    ok = 'OK' if raw_page.ok else 'NOT OK'
    print(f'Status code: {raw_page.status_code}[{ok}]')
    soup = BeautifulSoup(raw_page.text, 'html.parser')
    results_rows = results_rows + get_search_result_rows(soup, max-done)
    done = len(results_rows)
    if done < max:
        print(f'Completed: {done/max*100}%\nScrapping next page...\n----------------------------')
        next_page = get_next_page_url(soup)
        if not next_page:
            print(f'No more data found! [Total data scrapped: {done}]')
            return results_rows

        return scrap(next_page, max, results_rows)
    else:
        print(f'Completed: {done/max*100}%\n[DONE]\n----------------------------')
        return results_rows

        
if __name__ == '__main__':
    print('Running hamrobazar scrapy...')
    parser = argparse.ArgumentParser(description='Scrap hamrobazar data.')
    parser.add_argument('--search', type=str, help='search keyword[default={}]'.format(DEFAULT_SEARCH))
    parser.add_argument('--max', type=int, help='maximum search results to scrap[default={}]'.format(DEFAULT_MAX))
    parser.add_argument('--output', type=str, help='output filename[default={}]'.format(DEFAULT_FILENAME))

    args = parser.parse_args()
    search = args.search if args.search else DEFAULT_SEARCH
    filename =args.output if args.output else DEFAULT_FILENAME
    max = args.max if args.max else DEFAULT_MAX

    print(f'Search keyword: {search}    Max results: {max}\n------------------------------')
    hamroSearch = f'{BASE_SEARCH_URL}?do_search=Search&searchword={search}'

    result_rows = scrap(hamroSearch, max)
    json_data, data_keys = extract_data(result_rows)

    store_data_in_files(json_data, data_keys, filename)
    store_data_in_db(json_data, data_keys, filename)
    
