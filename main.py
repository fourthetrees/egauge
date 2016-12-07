#!/usr/bin/env python3
from src.egauge import query_dbfmt
from src.psql import exec_push
from os.path import dirname
import os
import time
import json

# Loage gauges and nonce.
def get_params():
    with open('tmp/gauges.json') as fp:
        gauges = json.load(fp)
    with open('tmp/auth.json') as fp:
        auth = json.load(fp)
    try:
        with open('tmp/nonce.txt') as fp:
            nonce = float(fp.read())
    except:
        nonce = time.time() - 86400
    return gauges,nonce,auth

# Query all gauges and return values.
def query_gauges(gauges,after=None):
    rows = []
    for g in gauges:
        rows += query_dbfmt(g,gauges[g],after)
    return rows

# Do something with the data.
def handle_data(data,auth):
    exec_push(data,auth)

# Update the nonce.
def update_nonce(nonce):
    with open('tmp/nonce.txt','w') as fp:
        fp.write(str(nonce))

# RunnnnN!!!
def Main():
    os.chdir(dirname(__file__))
    gauges,nonce,auth= get_params()
    data = query_gauges(gauges,after=nonce)
    nonce_new = max(data,key=lambda d: d.datetime).datetime
    handle_data(data,auth)
    update_nonce(nonce_new)

if __name__ == '__main__':
    Main()

