import csv
import json
import os
import re
import requests

url_strani = 'https://en.wikipedia.org/wiki/List_of_largest_sports_contracts'
#url glavne spletne strani

with open ("podatki_projekt_dodatno.html", encoding = 'utf-8') as f:
    vsebina_strani = f.read()

def shrani_klube_v_imenik(imenik):
    os.makedirs(imenik, exist_ok = True)
    stran = requests.get(url_strani)
    ime_datoteke = "podatki_projekt_dodatno.html"
    polna_pot_datoteke = os.path.join(imenik, ime_datoteke)
    with open(polna_pot_datoteke, 'w', encoding = 'utf-8') as datoteka:
        datoteka.write(stran.text)

re_podatki_pogodb = re.compile(
    '<tr>'
    '\n'
    '<td>(<.*"sorttext">)?(?P<Rank>\d+)(</span>.*)?</td>'
    '\n'
    '<td style="vertical-align:bottom;"><.*>(?P<Ime>.+)</a>(.*)?</td>'
    '\n'
    '<td style="vertical-align:bottom;"><.*>(?P<Klub>.+)</a>(.*)?</td>'
    '\n'
    '<td .*>(?P<Sport>.+?)<.*?'
    '\n'
    '<td .*</td>'
    '\n'
    '<td .*bottom;">(?P<Vrednost_pogodbe>.+?)<.*/td>'
    '\n'
    '<td .*bottom;">(?P<Vrednost_pogodbe_letno>.+?)<'
    )
#for ujemanje in re_podatki_transferjev.finditer(vsebina_strani):
    #print(ujemanje.groupdict())

#ujemanje = re.search('<td>.+</td>', vsebina_strani)
#print(ujemanje)

#shrani_klube_v_imenik('IMENIK')



for ujemanje in re_podatki_pogodb.finditer(vsebina_strani):
    print(ujemanje.groupdict())

def preberi_podatke(imenik):
    pogodbe = []
    ime_datoteke = "podatki_projekt_dodatno.html"
    polna_pot_datoteke = os.path.join(imenik,ime_datoteke)
    with open(polna_pot_datoteke, encoding ='utf8') as datoteka:
        vsebina_datoteke = datoteka.read()
        for ujemanje_1 in re_podatki_pogodb.finditer(vsebina_datoteke):
            if ujemanje_1:
                pogodba=ujemanje_1.groupdict()
                #klub['Ime'] = klub['Ime'].encode('utf-8').strip()
                if pogodba['Rank'] != None:
                    pogodba['Rank'] = int(pogodba['Rank'])
                if pogodba['Vrednost_pogodbe'] != None:
                    pogodba['Vrednost_pogodbe'] = pogodba['Vrednost_pogodbe'].strip('$')
                if pogodba['Vrednost_pogodbe'] != None:
                    pogodba['Vrednost_pogodbe'] = re.sub('[,+]', '',pogodba['Vrednost_pogodbe']) 
                if pogodba['Vrednost_pogodbe'] != None:
                    pogodba['Vrednost_pogodbe'] = int(pogodba['Vrednost_pogodbe'])
                if pogodba['Vrednost_pogodbe_letno'] != None:
                    pogodba['Vrednost_pogodbe_letno'] = pogodba['Vrednost_pogodbe_letno'].strip('$')
                if pogodba['Vrednost_pogodbe_letno'] != None:
                    pogodba['Vrednost_pogodbe_letno'] = re.sub('[,+]', '',pogodba['Vrednost_pogodbe_letno']) 
                if pogodba['Vrednost_pogodbe_letno'] != None:
                    pogodba['Vrednost_pogodbe_letno'] = int(pogodba['Vrednost_pogodbe_letno'])
                pogodbe.append(pogodba)
            else:
                print("neki ne deva tko k bi mogl")
            #klubi.append(podatki_klub(ujemanje_1))

    return pogodbe


Pogodbe = preberi_podatke('IMENIK')

def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)

Polja = ['Rank', 'Ime', 'Klub', 'Sport', 'Vrednost_pogodbe', 'Vrednost_pogodbe_letno']
zapisi_csv(Pogodbe, Polja, 'Pogodbe.csv')

import pandas as pd

tabela_pogodb = pd.read_csv('Pogodbe.csv', encoding = 'latin1')



