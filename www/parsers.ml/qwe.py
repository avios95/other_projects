#!/usr/bin/python3

import get_content
from bs4 import BeautifulSoup
import csv
import sys, json, base64, time


events_file = "arb_1x2" + ".csv"

data = json.loads(base64.b64decode(sys.argv[1]))
print(data)
vol = int(data[0])
percent = int(data[1])
cof_cof = float(data[2])




def get_table():
    referer = "https://www.google.com"
    url = "https://www.arbworld.net/en/moneyway/mw-1-x-2"
    r = get_content.get_content(url,referer)
    soup = BeautifulSoup(r.text, 'lxml')

    table1 = soup.find("table", {'class': 'grid'})
    for cof_list1 in table1.select("tr", {'class': 'heading'}):
        header_cof = []
        for cof1 in cof_list1.select("td"):
            header_cof.append(cof1.get_text(separator=' '))
    
    with open(events_file, 'w') as csvfile:
        writercol = csv.DictWriter(csvfile, fieldnames=header_cof[3:14])
        writercol.writeheader()

    table = soup.find('table', {'id': 'matches' })

    for cof_list in table.select("tr", {'class': 'belowHeader'}):
        cof_list_list = []
        for cof in cof_list.select("td"):
            cof_list_list.append(cof.get_text(separator=' '))

        if len(cof_list_list[2:13]) == 0: continue
        
        if int(cof_list_list[12].replace('€', '').replace(' ', '')) > vol:
            if float(cof_list_list[9].replace('€', '').replace('%', '').split()[0]) > percent:
                if float(cof_list_list[6]) > cof_cof:
                    with open(events_file, 'a') as csvfile:
                        writerrow = csv.writer(csvfile)
                        writerrow.writerow(cof_list_list[2:13])
            if float(cof_list_list[10].replace('€', '').replace('%', '').split()[0]) > percent:
                if float(cof_list_list[7]) > cof_cof:
                    with open(events_file, 'a') as csvfile:
                        writerrow = csv.writer(csvfile)
                        writerrow.writerow(cof_list_list[2:13])
                        print(cof_list_list)
            if float(cof_list_list[11].replace('€', '').replace('%', '').split()[0]) > percent:
                if float(cof_list_list[8]) > cof_cof:
                    with open(events_file, 'a') as csvfile:
                        writerrow = csv.writer(csvfile)
                        writerrow.writerow(cof_list_list[2:13])


get_table()


filein = open(events_file, "r")
fileout = open("table1x2.html", "w")
data = filein.readlines()

table = "<table>\n"

# Create the table's column headers
header = data[0].split(",")
table += "  <tr>\n"
for column in header:
    table += "    <th>{0}</th>\n".format(column.strip())
table += "  </tr>\n"

# Create the table's row data
for line in data[1:]:
    row = line.split(",")
    table += "  <tr>\n"
    for column in row:
        table += "    <td>{0}</td>\n".format(column.strip())
    table += "  </tr>\n"

table += "</table>"

fileout.writelines(table)
fileout.close()
filein.close()
