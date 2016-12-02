#!/usr/bin/env python3
import requests

def query(gauge,start=None,stop=None):
    uri = 'http://egauge{}.egaug.es/cgi-bin/egauge-show?c&C'
    if start and stop:
        uri += ''
    r = requests.get(uri.format(gauge))
    rows = [[y for y in x.split(',')]
            for x in r.text.splitlines()]
    headers = rows.pop(0)
    columns = list(zip(*rows))
    return {h: list(map(float,columns[i])) for i,h in enumerate(headers)}

def dbfmt(data):
    if not 

def scrape(guage,start=None,stop=None):
    data = query(quage,start,stop)
    return dbfmt(data)

#def scrape(gauge,start,stop):
