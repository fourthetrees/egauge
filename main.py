#!/usr/bin/env python3
from src.egauge import query_dbfmt
from src.psql import exec_push
from src.qlog import mklog
from os.path import dirname
import os
import time
import json

# Loage gauges and nonce.
def get_params():
    with open('tmp/gauges.json') as fp:
        gauges = json.load(fp)
    try:
        with open('tmp/nonce.json') as fp:
            nonce = json.load(fp)
    except:
        nonce = {}
    delta =  time.time() - 86400
    for g in (x for x in gauges if not x in nonce):
        nonce[g] = delta
    return gauges,nonce

# Query all gauges and return values.
def query_gauges(gauges,nonce):
    rows = []
    nonce_new = {}
    for g in gauges:
        r = query_dbfmt(g,gauges[g],nonce[g])
        nonce_new[g] = max(r,key=lambda x: x.datetime).datetime if r else nonce[g]
        rows += r
    return rows, nonce_new

# Do something with the data.
def handle_data(data):
    exec_push(data)

# Update the nonce.
def update_nonce(nonce_new):
    with open('tmp/nonce.json','w') as fp:
        json.dump(nonce_new,fp)

# RunnnnN!!!
def run():
    os.chdir(dirname(__file__))
    gauges,nonce= get_params()
    data,nonce_new = query_gauges(gauges,nonce)
    handle_data(data)
    update_nonce(nonce_new)

def Main():
    try:
        run()
    except Exception as err:
        mklog(err)

if __name__ == '__main__':
    Main()

