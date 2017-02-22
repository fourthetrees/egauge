#!/usr/bin/env python3
import time
import csv
import os

# Generate and update a simple and readable log file.
def mklog(project,text):
    hdr  = 'logtime............{}'.format(int(time.time()))
    proj = 'project............{}'.format(project)
    ftr  = '...................endlog\n'
    if project in os.listdir('tmp/projects/'):
        fpath = 'tmp/projects/{}/err_log.txt'.format(project)
    else: fpath = 'tmp/err_log.txt'
    with open(fpath,'a') as fp:
        write = lambda txt: print(txt,file=fp)
        write(hdr)
        write(proj)
        write(text)
        write(ftr)

# write a csv of improperly formatted
# data to an appropriate errors file.
def fmterr(project,data,txt='fmterr'):
    projdir = 'tmp/errors/{}/'.format(project)
    if not project in os.listdir('tmp/errors/'):
        os.mkdir(projdir)
    fname = projdir + txt + '-'+ str(time.time()) + '.csv'
    fields = data[0]._fields
    with open(fname,'w') as fp:
        print('writing {} malformed rows to: {}'.format(len(data),fname))
        writer = csv.writer(fp)
        writer.writerow(fields)
        for d in data: writer.writerow(d)
