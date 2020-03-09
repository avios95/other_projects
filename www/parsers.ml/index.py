#!/usr/bin/python3

import get_content
from bs4 import BeautifulSoup

print("Content-type: text/html; charset=utf-8\n\n")
def get_table():
    print("""
<html>
<head>
<title>Parser arbworld.net</title>
</head>
<body>
<a href="https://www.arbworld.net/en/moneyway/mw-1-x-2">arbworld.net  1x2</a>
<h3>Table 1x2</h3><br>

""")



    vol=10000
    percent=70
    cof_cof=1.8

    referer = "https://www.google.com"
    url = "https://www.arbworld.net/en/moneyway/mw-1-x-2"
    r = get_content.get_content(url,referer)
    soup = BeautifulSoup(r.text, 'lxml')


    table1 = soup.find("table", {'class': 'grid'})
    for cof_list1 in table1.select("tr", {'class': 'heading'}):
        header_cof = []
        for cof1 in cof_list1.select("td"):
            header_cof.append(cof1.get_text(separator=' '))

    print(header_cof[3:14],"<br><br>")

    table = soup.find('table', {'id': 'matches' })

    for cof_list in table.select("tr", {'class': 'belowHeader'}):
        cof_list_list = []
        for cof in cof_list.select("td"):
            cof_list_list.append(cof.get_text(separator=' '))

        if len(cof_list_list[2:13]) == 0: continue
        if int(cof_list_list[12].replace('€', '').replace(' ', '')) > vol:
            if float(cof_list_list[9].replace('€', '').replace('%', '').split()[0]) > percent:
                if float(cof_list_list[6]) > cof_cof:
                    print(cof_list_list[2:13],"<br>")
            if float(cof_list_list[10].replace('€', '').replace('%', '').split()[0]) > percent:
                if float(cof_list_list[7]) > cof_cof:
                    print(cof_list_list[2:13],"<br>")
            if float(cof_list_list[11].replace('€', '').replace('%', '').split()[0]) > percent:
                if float(cof_list_list[8]) > cof_cof:
                    print(cof_list_list[2:13],"<br>")


html = """
{TABLE}
</body>
</html>
""".format(TABLE=get_table())
print(html)
