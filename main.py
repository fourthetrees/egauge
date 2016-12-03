#!/usr/bin/env python3
from src.egauge import query_dbfmt
import time
import json

# Loage gauges and nonce.
def get_params():
    with open('tmp/gauges.json') as fp:
        gauges = json.load(fp)
    try:
        with open('tmp/nonce.txt') as fp:
            nonce = float(fp.read())
    except:
        nonce = time.time() - 86400
    return gauges,nonce

# Query all gauges and return values.
def query_gauges(gauges,after=None):
    rows = []
    for g in gauges:
        rows += query_dbfmt(g,gauges[g],after)
    return rows

# Do something with the data.
def handle_data(data):
    for i in range(10):
        print(data[i])

# Update the nonce.
def update_nonce(nonce):
    with open('tmp/nonce.txt','w') as fp:
        fp.write(str(nonce))

def Main():
    gauges,nonce = get_params()
    data = query_gauges(gauges,after=nonce)
    nonce_new = max(data,key=lambda d: d.datetime).datetime
    handle_data(data)
    update_nonce(nonce_new)


if __name__ == '__main__':
    Main()

