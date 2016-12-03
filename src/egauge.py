#!/usr/bin/env python3
from collections import namedtuple
import requests

# Query a specified egauge.
# Returns a dictionary of all columns w/ headers as keys.
def query(gauge,after=None):
    uri = 'http://egauge{}.egaug.es/cgi-bin/egauge-show?c&C&m'
    if after: params = {'w':after}
    else: params = None
    r = requests.get(uri.format(gauge),params=params)
    rows = [[y for y in x.split(',')] for x in r.text.splitlines()]
    headers = [x.replace('"','') for x in rows.pop(0)]
    columns = list(zip(*rows))
    return {h: list(map(float,columns[i])) for i,h in enumerate(headers)}



# Convert into row format.
# Returns list of named tuples.
def dbfmt(gauge_id,gauge,data):
    row = namedtuple('row',['datetime','sensor_id','enduse','value'])
    dtimes = data['Date & Time']
    values = {k: data[k] for k in data if k != 'Date & Time'}
    sn_id = gauge_id + '_{}'.format(gauge)
    rows = []
    for vt in values:
        fmt = lambda dt,val: row(dt, sn_id, vt, val)
        rows += [fmt(t,p) for t,p in zip(dtimes,values[vt])]
    return rows

# Query egauge and return vals in formatted rows.
# This is just a useful composition of the query and dbfmt functions.
def query_dbfmt(gauge_id,gauge,after=None):
    data = query(gauge,after)
    return dbfmt(gauge_id,gauge,data)

