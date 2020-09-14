import os
import time
import csv
import json
from yaml import dump
#from lxml.etree import Element, xmlfile
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

directoryname='output'
outputpath=os.path.join(os.getcwd(),directoryname)
page_numbers=[1,2,3,4]

#create a folder output in specified path
def create_output_folder():
    if os.path.exists(outputpath)== False:  
        os.makedirs(directoryname)
    else:
        print("The folder already exists")

#scrape books
def scrape_books(page_number):
    books_stock=[]
    #scrape books stock from books.toscrape.com
    url= 'http://books.toscrape.com/catalogue/page-'
    #pass page number in request
    request = requests.get(url+str(page_number)+'.html')
    print(request)
    soup= BeautifulSoup(request.content,'html.parser')
    content=soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for book in content:
        book_name=book.find('h3').text
        price=book.find('p',class_='price_color').text
        
        book_info={
        'book_name': book_name,
        'price': price,
        }
        books_stock.append(book_info)
    return books_stock

#write the scraped data to csv file
def write_list_to_csv_file(page_number):
    csvfilename=os.path.join(outputpath,"filename.csv")
    with open(csvfilename, "a", newline='') as csvfile:  
        fieldnames = ['book_name', 'price']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for books in scrape_books(page_number):
            writer.writerow(books)

#write the scraped data to json file
def write_list_to_json_file(page_number):
    jsonfilename=os.path.join(outputpath,"filename.json")
    book_stock_json = {
        "book_in_stock":scrape_books(page_number) 
    }
    with open(jsonfilename, 'a+') as jsonfile:
        json.dump(book_stock_json, jsonfile, indent = 2,ensure_ascii=True)


#write the scraped data to yaml file
def write_list_to_yaml_file(page_number):
    yamlfilename=os.path.join(outputpath,"filename.yaml")
    with open(yamlfilename, 'a') as yamlfile:
        dump(data=scrape_books(page_number), stream=yamlfile)

# write the scraped data to xml file
"""def write_list_to_xml_file(books_stock):
    xmlfilename=os.path.join(outputpath,"filename.xml")
    elem_keys = list(books_stock[0].keys())
    print(elem_keys)
    root= Element('book_in_stock')

    for books in books_stock:
        elem=Element(key)
        elem.text=books(key)
        sub_elem.append(elem)

    root.append(sub_elem)
    with xmlfile(xmlfilename, encoding='utf-8') as xmlfiles:
        xmlfiles.write_declaration(standalone=True)
        xmlfiles.write(root)    
"""
if __name__=='__main__':
    create_output_folder()
  #  write_list_to_xml_file(books_stock)
    with Pool(len(page_numbers)) as p:
        p.map(write_list_to_csv_file,page_numbers)
        p.map(write_list_to_json_file,page_numbers)
        p.map(write_list_to_yaml_file,page_numbers)
