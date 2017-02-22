#!/usr/bin/env python3
from collections import namedtuple
from src.data_structs import Row
import requests

# Query all gauges and return values.
# Returns rows in format:
# ('node','sensor','unit','timestamp','value')
def query_gauges(gauges,nonce):
    rows = []
    nonce_new = {}
    for gid in gauges:
        raw = query(gauges[gid],nonce[gid])
        data = fmt_query(gid,raw)
        nonce_new[gid] = max(data,key=lambda x: x.timestamp).timestamp if data else nonce[gid]
        rows += data
    return rows, nonce_new

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
def fmt_query(gauge_id,data):
    dtimes = data['Date & Time']
    values = {k: data[k] for k in data if k != 'Date & Time'}
    formatted = []
    for sn in values:
        unit,snid = parse_sntxt(sn)
        fmt = lambda t,v: Row(gauge_id,snid,unit,t,v)
        formatted += [fmt(t,v) for t,v in zip(dtimes,values[sn])]
    return formatted

# Split the egauge supplied sensor/column name
# into separate units and sensor id.
def parse_sntxt(sensor):
    try:
        unit = sensor.split('[').pop().replace(']','').replace(' ','')
        snid = sensor.split(' [').pop(0).lower()
    except Exception as err:
        print('failed to parse: {}'.format(sensor))
        print('parse error: {}'.format(err))
        unit = 'undefined'
        snid = sensor.lower()
    return unit,snid
