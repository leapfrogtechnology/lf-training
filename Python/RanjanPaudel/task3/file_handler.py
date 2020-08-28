import csv
import json
from yaml import dump
from lxml.etree import Element, xmlfile

if __name__ == "file_handler":
    def store_in_csv(data_list, filename):
        headers = list(data_list[0].keys())

        with open(filename, 'w', newline='') as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames=headers, quotechar='"', delimiter=',')

            csv_writer.writeheader()
            csv_writer.writerows(data_list)

    def store_in_json(data_list, filename):
        movie_list_type = filename.split('/')[1]
        json_data = {
            movie_list_type: data_list
        }
        with open(filename, 'w') as json_file:
            json.dump(json_data, json_file)

    def store_in_xml(data_list, filename):
        movie_list_type = filename.split('/')[1]
        elem_keys = list(data_list[0].keys())

        root = Element(movie_list_type)

        for data in data_list:
            sub_elem = Element('movie')

            for key in elem_keys:
                elem = Element(key)
                elem.text = data[key]
                sub_elem.append(elem)

            root.append(sub_elem)

        with xmlfile(filename, encoding='utf-8') as xml_file:
            xml_file.write_declaration(standalone=True)
            xml_file.write(root)

    def store_in_yaml(data_list, filename):
        movie_list_type = filename.split('/')[1]
        yaml_data = {
            movie_list_type: data_list
        }

        with open(filename, 'w') as yaml_file:
            dump(data=yaml_data, stream=yaml_file)
