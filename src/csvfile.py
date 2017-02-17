#!/usr/bin/env python3
import csv

def to_csv(data,fname):
    fields = data[0]._fields
    if not '.csv' in fname:
        fname += '.csv'
    with open(fname,'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(fields)
        for d in data: writer.writerow(d)
