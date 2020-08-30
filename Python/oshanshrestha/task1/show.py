import os
import csv
import argparse

def showresults(fileName):
    with open (fileName,"r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        results = ''
        for row in csv_reader:
            results += "Name: {}".format(row["name"]) + "\n"
            results += "Date of Birth: {}".format(row["dob"].split(' ')[0]) + "\n"
            results += row["subject"] + ":\n"
            results += "\t"+"Score: {}".format(row["score"]) + "\n"
            results += "\t"+"Total: {}".format(row["total"]) + "\n"
            results += "Percentage: {}".format(row["percentage"]) + "\n"
            results += "-----------------"+ "\n\n"
        csvfile.close()
        return results

parser = argparse.ArgumentParser()
parser.add_argument("--store", help="Enter filename")

args = parser.parse_args()

filename = args.store

if os.path.exists(filename):
    print(showresults(filename))

else:
    print("File %s not found" %(filename))
