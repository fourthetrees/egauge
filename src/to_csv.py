#!/usr/bin/env python3
from collections import namedtuple
from src.errlog import fmterr
import time
import csv
import os
import os.path as path

# Main save-to-csv entry point.
# Handles formatting, calculated fields, etc...
# Conforums to guideline that all destination
# functions should have required args of the
# form: (data,project,config).
def to_csv(data,project,csv_config,ftxt='output'):
    # TODO: use csv config values for something...
    # probably for choosing file txt, etc...
    save_csv(data,project,ftxt)

# Save it to a thing!
def save_csv(data,project,ftxt):
    projdir = dirset(project)
    fname = fset(ftxt)
    fpath = projdir + fname
    fields = data[0]._fields
    print('writing {} rows to {}'.format(len(data),fpath))
    with open(fpath,'w') as fp:
        writer = csv.writer(fp)
        writer.writerow(fields)
        for d in data: writer.writerow(d)

# set up & return project output dir.
def dirset(project):
    projdir = 'tmp/outputs/{}/'.format(project)
    if not path.isdir(projdir):
        os.makedirs(projdir)
    return projdir

# set up & return file name.
def fset(ftxt):
    ft = str(int(time.time()))
    fname = '{}-{}.csv'.format(ftxt,ft)
    return fname
