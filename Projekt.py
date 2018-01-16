import csv
import json
import os
import re
import requests

with open ("podatki.html", encoding = 'utf-8') as f:
    vsebina_strani = f.read()

re_podatki_klubov = re.compile(
    '(<td( rowspan="\d+")?>(?P<Rang>.+)</td>)?'
    '\n?'
    '(<td(\.+)?>\d+</td>)?'
    '<td><a href="(.+)" title="(.+)">'
    '(?P<Ime>.+)' #ime kluba
    '</a></td>'
    '\n'
    '<td>(?P<Sport>.+)</td>'
    '\n'
    '.*?'
    'title="(.+)">(?P<Drzava>.+)</a></td>'
    '\n'
    '(<td( rowspan="\d+")?>(?P<Vrednost>.+)</td>)?'
    )

#for ujemanje in re_podatki_klubov.finditer(vsebina_strani):
    
    #print(ujemanje.groupdict())

def shrani_klube_v_imenik(imenik):
    os.makedirs(imenik, exist_ok = True)
    stran = requests.get('https://en.wikipedia.org/wiki/Forbes%27_list_of_the_most_valuable_sports_teams')
    ime_datoteke = "podatki_projekt.html"
    polna_pot_datoteke = os.path.join(imenik, ime_datoteke)
    with open(polna_pot_datoteke, 'w', encoding = 'utf-8') as datoteka:
        datoteka.write(stran.text)


def preberi_podatke(imenik):
    klubi = []
    ime_datoteke = "podatki_projekt.html"
    polna_pot_datoteke = os.path.join(imenik,ime_datoteke)
    with open(polna_pot_datoteke, encoding ='utf8') as datoteka:
        vsebina_datoteke = datoteka.read()
        for ujemanje_1 in re_podatki_klubov.finditer(vsebina_datoteke):
            if ujemanje_1:
                klub=ujemanje_1.groupdict()
                #klub['Ime'] = klub['Ime'].encode('utf-8').strip()
                if klub['Rang'] != None:
                    klub['Rang'] = float(klub['Rang'])
                if klub['Vrednost'] != None:
                    klub['Vrednost'] = float(klub['Vrednost'])
                klubi.append(klub)
            else:
                print("neki ne deva tko k bi mogl")
            #klubi.append(podatki_klub(ujemanje_1))

    return klubi

def zapisi_json(podatki, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        json.dump(podatki, datoteka, indent=2)


def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)

    
#shrani_klube_v_imenik('IMENIK')
Klubi = preberi_podatke('IMENIK')
#zapisi_json(Klubi, "Klubi.json")

Polja = ['Rang', 'Ime', 'Sport', 'Drzava', 'Vrednost']
zapisi_csv(Klubi, Polja, 'Klubi.csv')

import pandas as pd

tabela = pd.read_csv('Klubi.csv', encoding = 'latin1')

    
