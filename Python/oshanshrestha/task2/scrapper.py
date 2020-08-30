import os
import time
import csv
import json
from yaml import dump
import requests
from bs4 import BeautifulSoup


foldername='output'
folderpath=os.path.join(os.getcwd(),foldername)

def create_output_folder():
    if os.path.exists(folderpath)== False:
        os.makedirs(foldername)
    else:
        print("Folder already exists!!")

scraped_books=[]
for x in range(1,2):
    url= 'http://books.toscrape.com/catalogue/page-'
    request = requests.get(url+str(x)+'.html')
    soup= BeautifulSoup(request.content,'html.parser')
    content=soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')

    for book in content:
        book_name=book.find('h3').text
        cost=book.find('p',class_='price_color').text

        book_info={
        'book_name': book_name,
        'cost': cost,
        }

        scraped_books.append(book_info)
    time.sleep(2)

#write the scraped data to csv file
def store_csv_file(scraped_books):
    csvfilename=os.path.join(folderpath,"bookinfo.csv")
    with open(csvfilename, "w", newline='') as csvfile:
        fieldnames = ['book_name', 'cost']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for books in scraped_books:
            writer.writerow(books)

#write the scraped data to json file
def store_json_file(scraped_books):
    jsonfilename=os.path.join(folderpath,"bookinfo.json")
    book_stock_json = {
          "book_in_stock": scraped_books
      }
    with open(jsonfilename, 'w') as jsonfile:
        json.dump(book_stock_json, jsonfile, indent = 2,ensure_ascii=True)

#write the scraped data to yaml file
def store_yaml_file(scraped_books):
    yamlfilename=os.path.join(folderpath,"bookinfo.yaml")
    with open(yamlfilename, 'w') as yamlfile:
        dump(data=scraped_books, stream=yamlfile)



if __name__=='__main__':
    create_output_folder()
    store_csv_file(scraped_books)
    store_json_file(scraped_books)
    store_yaml_file(scraped_books)
