#!/usr/bin/env python3
import subprocess as sp
import os

uri = "/home/forrest/Code/csbcd/egauge/"

os.chdir(uri)

# os.system('./main.py')
try:
    sp.run('./main.py',check=True)
except Exception as err:
    with open('tmp/log.txt','a') as fp:
        fp.write(err.stdout)
