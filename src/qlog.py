#!/usr/bin/env python3
import time

# Generate and update a simple and readable log file.
def mklog(text):
    hdr = 'logtime............{}'.format(int(time.time()))
    ftr = '...................endlog\n'
    with open('tmp/log.txt','a') as fp:
        print(hdr,file=fp)
        print(text,file=fp)
        print(ftr,file=fp)
