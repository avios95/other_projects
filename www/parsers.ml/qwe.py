#!/usr/bin/python3

import get_content, csv, sys, json, base64, requests, time
from bs4 import BeautifulSoup

data = json.loads(base64.b64decode(sys.argv[1]))
print(data)
vol = int(data[0])
percent = int(data[1])
cof_cof = float(data[2])
drop = float(data[3])
filein1 = "arb_1x2.csv"
fileout1 = "table1x2.html"
filein2 = "droppingodds.csv"
fileout2 = "droppingodds.html"
filein3 = "merge.csv"
fileout3 = "merge.html"


def sendtelegram(text):
    url = "https://api.telegram.org/bot935741304:AAEWIRYatYV3pFCYkdsGE781lEZf49xsR4I/sendMessage"
    data = {'chat_id': "262937164",
            'text': text}
    requests.post(url, data=data)


def generate_xml_table(file1, file2):
    filein = open(file1, "r")
    fileout = open(file2, "w")
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


def get_table_1x2():
    referer = "https://www.google.com"
    url = "https://www.arbworld.net/en/moneyway/mw-1-x-2"
    r = get_content.get_content(url, referer)
    soup = BeautifulSoup(r.text, 'lxml')
    events_file = filein1

    table1 = soup.find("table", {'class': 'grid'})
    for cof_list1 in table1.select("tr", {'class': 'heading'}):
        header_cof = []
        for cof1 in cof_list1.select("td"):
            header_cof.append(cof1.get_text(separator=' '))

    with open(events_file, 'w') as csvfile:
        writercol = csv.DictWriter(csvfile, fieldnames=header_cof[3:14])
        writercol.writeheader()

    table = soup.find('table', {'id': 'matches'})

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
            if float(cof_list_list[11].replace('€', '').replace('%', '').split()[0]) > percent:
                if float(cof_list_list[8]) > cof_cof:
                    with open(events_file, 'a') as csvfile:
                        writerrow = csv.writer(csvfile)
                        writerrow.writerow(cof_list_list[2:13])


def get_table_droppingodds():
    referer = "https://www.google.com"
    url = "https://www.arbworld.net/en/droppingodds"
    r = get_content.get_content(url, referer)
    soup = BeautifulSoup(r.text, 'lxml')
    events_file = filein2

    table1 = soup.find("table", {'class': 'grid'})
    for cof_list1 in table1.select("tr", {'class': 'heading'}):
        header_cof = []
        for cof1 in cof_list1.select("td"):
            header_cof.append(cof1.get_text(separator=' '))

    with open(events_file, 'w') as csvfile:
        writercol = csv.DictWriter(csvfile, fieldnames=header_cof[3:14])
        writercol.writeheader()

    table = soup.find('table', {'id': 'matches'})

    for cof_list in table.select("tr", {'class': 'belowHeader'}):
        cof_list_list = []
        for cof in cof_list.select("td"):
            cof_list_list.append(cof.get_text(separator=' '))

        if len(cof_list_list[2:13]) == 0: continue
        if float(cof_list_list[6].split()[0]) - float(cof_list_list[6].split()[1]) >= drop:
            with open(events_file, 'a') as csvfile:
                writerrow = csv.writer(csvfile)
                row = cof_list_list[2], cof_list_list[3], cof_list_list[4], cof_list_list[5], cof_list_list[
                    6], "", "", "", "", cof_list_list[11], cof_list_list[12]
                writerrow.writerow(row)

        if float(cof_list_list[8].split()[0]) - float(cof_list_list[8].split()[1]) >= drop:
            with open(events_file, 'a') as csvfile:
                writerrow = csv.writer(csvfile)
                row = cof_list_list[2], cof_list_list[3], cof_list_list[4], cof_list_list[5], "", "", cof_list_list[
                    8], "", "", cof_list_list[11], cof_list_list[12]
                writerrow.writerow(row)

        if float(cof_list_list[10].split()[0]) - float(cof_list_list[10].split()[1]) >= drop:
            with open(events_file, 'a') as csvfile:
                writerrow = csv.writer(csvfile)
                row = cof_list_list[2], cof_list_list[3], cof_list_list[4], cof_list_list[5], "", "", "", "", \
                      cof_list_list[10], cof_list_list[11], cof_list_list[12]
                writerrow.writerow(row)


def get_table_marge_telegram():
    with open(filein2, "r") as file1:
        read1 = csv.reader(file1, delimiter=',')
        for row1 in read1:
            with open(filein1, "r") as file2:
                read2 = csv.reader(file2, delimiter=',')
                for row2 in read2:
                    if row2[2].strip() in row1[2].strip() and row2[3].strip() in row1[9].strip():
                        text = row2 + row1[4:9]
                        if row2[2].strip() in "Home":
                            continue
                        a = ''
                        for i in text:
                            a = a + i + " "

                        sendtelegram(a)


def get_table_marge():
    with open(filein2, "r") as file1:
        read1 = csv.reader(file1, delimiter=',')
        for row1 in read1:
            with open(filein1, "r") as file2:
                read2 = csv.reader(file2, delimiter=',')
                for row2 in read2:
                    if row2[2].strip() in row1[2].strip() and row2[3].strip() in row1[9].strip():
                         if row2[2].strip() in "Home":
                            with open(filein3, 'w') as csvfile:
                               writerrow = csv.writer(csvfile)
                               text = row2 + row1[4:9]
                               writerrow.writerow(text)
                         else: 
                            with open(filein3, 'a') as csvfile:
                               writerrow = csv.writer(csvfile)
                               text = row2 + row1[4:9]
                               writerrow.writerow(text)


get_table_1x2()
get_table_droppingodds()
get_table_marge_telegram()
get_table_marge()
generate_xml_table(filein1, fileout1)
generate_xml_table(filein2, fileout2)
generate_xml_table(filein3, fileout3)
