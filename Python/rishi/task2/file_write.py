import csv
import yaml
import json

from utils import CsvCreator, get_filepath_name
from config import DIRECTORY_PATH, OUTPUT_FILE

fieldname = [
             'brand',
             'title',
             'price',
             'aggregateRating',
             'image_url',
             'description',
             'url_link'
             ]

def write_empty_result_sets(empty_search_result_list):
    filepath = get_filepath_name('empty_result.csv')
    with open(filepath, mode='w') as wr:
        writer = csv.writer(wr, quoting=csv.QUOTE_ALL)
        writer.writerow(empty_search_result_list)

def write_overall_result(contents):
    filepath = get_filepath_name(OUTPUT_FILE)
    op = CsvCreator(filepath, fieldname)
    for key, rows in contents.items():
        for row in rows:
            op.write_to_file(row)
    return

def write_to_csv(fp, contents):
    filepath = get_filepath_name(fp)
    output_file_handle = CsvCreator(filepath, fieldname)
    for brand, rows in contents.items():
        for row in rows:
            output_file_handle.write_to_file(row)
    return

def write_to_yaml(fp, contents):
    filepath = get_filepath_name(fp) + '.yaml'
    with open(filepath, 'w') as file_:
        yaml.dump(contents, file_)

def write_to_json(fp, contents):
    filepath = get_filepath_name(fp) + '.json'
    with open(filepath, 'w') as json_file:
        json.dump(contents, json_file)