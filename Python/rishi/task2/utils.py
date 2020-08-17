import csv

class CsvCreator:
    def __init__(self, filename, headers):
        self.filename = filename
        self.headers = headers
        self.createfile()
    
    def createfile(self):
        with open(self.filename, mode='w') as csv_file:
            writer =csv.DictWriter(csv_file, fieldnames=self.headers)
    
    def write_to_file(self, row):
        with open(self.filename, mode='a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.headers)
            writer.writerow(row)