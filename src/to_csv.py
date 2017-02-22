#!/usr/bin/env python3
from collections import namedtuple
from src.errlog import fmterr
import time
import csv
import os

# Main save-to-csv entry point.
# Handles formatting, calculated fields, etc...
# Conforums to guideline that all destination
# functions should have required args of the
# form: (data,project,config).
def to_csv(data,project,csv_config):
    # TODO: use csv config values for something...
    fname = '{}.csv'.format(time.time())
    save_csv(data,project,fname)

# Save it to a thing!
def save_csv(data,project,fname):
    projdir = 'tmp/outputs/{}/'.format(project)
    if not project in os.listdir('tmp/outputs/'):
        os.mkdir(projdir)
    if not '.csv' in fname:
        fname = fname + '.csv'
    fdir = projdir + fname
    fields = data[0]._fields
    with open(fdir,'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(fields)
        for d in data: writer.writerow(d)
