#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# zależności Pythona: BeatifulSoup
# instalacja z pakietu
# Debian /Ubuntu: apt-get install python-bs4
# albo
# easy_install beautifulsoup4
# lub
# pip install beautifulsoup4

# skrypt robi spis firm ze stron mambiznes.pl
# i wypluwa CSV:
# Kolumny:
# fid
# nazwa - Nazwa firmy
# url   - url do strony w mambiznes.pl
# opis  - skrócony opis
# full  - link do lokalnego pliku z pełnym opisem
# ourl  - url do oryginalnej strony firmy

import sys
import urllib2
import random
from time import sleep
from bs4 import BeautifulSoup
from bs4 import SoupStrainer

# identyfikator firmy
fid = 0
# ile stron ma indeks na mambiznes.pl (trzeba sprawdzać ręcznie)
# dziś (18.09.2017) jest 53
ILE_STRON = 53
# plik z indeksem firm
CSV_FILE = "startupy.csv"
# parametr do sleep() do oszukiwania firewalli
MNOZNIK = 10
# nagłówek każdego pliku z pełnym opisem firmy
html_header = """
<!DOCTYPE html>
<html lang="pl-PL">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="mambiznes.css" type="text/css">
"""
html_footer = """
</body>
</html>
"""

# zawężam wyszukiwanie na stronach indeksów do diva "main"
only_main = SoupStrainer("main")
# zawężam wyszukiwanie na stronie firmy do diva z klasą
only_opis = SoupStrainer("div", class_="post-desc np")

# ćwiczę na lokalnym pliku
#plik = open('test.html', 'r').read()
#artin = (BeautifulSoup(plik, "html.parser", parse_only=only_main))


# wypluwam CSV
def skanuj(artin):
    global fid
    linia = ""
    for x in  artin.find_all("div", class_="article-bottom"):
        fid += 1
        sys.stdout.write('.')
        sys.stdout.flush()
        opis_file = str(fid) + ".html"
        url = x.find('a', class_='dib title').get('href')
        nazwa = x.find('a', class_='dib title').contents[0]
        linia += \
                '"' + \
                str(fid) + \
                '","' + \
                nazwa + \
                '","' + \
                url + \
                '","' + \
                x.find('p', class_="excerpt").contents[0] + \
                '","' + \
                opis_file + \
                '",""' + \
                "\n"
        # trzeba pobrać pełny opis firmy
        # opóźnienie żeby zmylić ew. proxy
        sleep(random.random() * MNOZNIK/1.3)
        opis_url = urllib2.urlopen(url)
        opis = (BeautifulSoup(opis_url, "html.parser", parse_only=only_opis))
        plout = open(opis_file, 'w')
        txtout = html_header + "<title>" + nazwa.encode('utf-8') + "</title>\n</head>\n\n<body>" + str(opis) + html_footer
        plout.write(str(txtout))
        plout.close()
    return linia.encode('utf-8')

# pobieram dane z portalu
print "Pobieram strone:"
out = "fid,nazwa,url,opis,full,ourl\n"
for  i in range(1, ILE_STRON+1):
    sys.stdout.write(str(i))
    sys.stdout.flush()
    weburl = "https://mambiznes.pl/startupy/page/" + str(i)
    data = urllib2.urlopen(weburl)
    artin = (BeautifulSoup(data, "html.parser", parse_only=only_main))
    out += skanuj(artin)
    sys.stdout.write('done\n')
    sys.stdout.flush()
#print out
# można do pliku, żeby mieć to w d.
fout = open(CSV_FILE, 'w')
fout.write(out)
fout.close()
