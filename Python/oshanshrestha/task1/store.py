import sys
import argparse
from datetime import datetime
import csv
import operator
import os

#Convert to datetime type
def dob(value):
    return datetime.strptime(value,'%d/%m/%Y')

#Calculate percentage
def calcpercentage(total, score):
    return ((score/total)*100)

#Duplicate Check
def isDuplicate(args):
    with open(args.store, mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            if row["name"] == args.name and row["subject"]== args.subject: #Checking for Name and Subject
                return True
    return False

def writeFile(file, args):
        thewriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        thewriter.writerow([args.name, args.dob, args.subject, args.total, args.score, calcpercentage(args.total,args.score)])

def addheader(file, args):
        thewriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        thewriter.writerow(["name", "dob", "subject", "total", "score", "percentage"])

parser = argparse.ArgumentParser(description='Scoresheet')
parser.add_argument('name', type=str, help='Student Name')
parser.add_argument('dob', type=dob, help='Date of Birth dd/mm/yy')
parser.add_argument('subject', choices=['English','Mathematics','Nepali'], help='One of the subjects')
parser.add_argument('total', type=float,  help='Total Score')
parser.add_argument('score', type=float, help='Marks Scored')
parser.add_argument("store", type=str, help="Enter filename")
args = parser.parse_args()

filename=args.store

if os.path.exists(filename):
    file=open(filename,"a")
    if isDuplicate(args):
        print("Duplicate Record")
    else:
        writeFile(file, args)

else:
    file = open(filename, "w")
    addheader(file, args)
    writeFile(file, args)
