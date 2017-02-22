#!/usr/bin/env python3
import os.path as path
import time
import os
import json

# Loage gauges and nonce.
def get_params(project):
    check_proj(project)
    config = get_config(project)
    nonce = get_nonce(project,config['gauges'])
    return config,nonce

# Check if project file exists
def check_proj(project):
    projects = os.listdir('tmp/projects/')
    if not project in projects:
        raise Exception('no project named {}'.format(project))

# get project configuration
def get_config(project):
    fpath = 'tmp/projects/{}/config.json'.format(project)
    if not path.isfile(fpath):
        raise Exception('no config found for {}.'.format(project))
    with open(fpath) as fp:
        config = json.load(fp)
    if not "gauges" in config:
        raise Exception('no "gauges" field in config for {}'.format(project))
    return config

# get nonce data and autofill
# any unfilled nonces.
def get_nonce(project,gauges):
    fpath = 'tmp/projects/{}/nonce.json'.format(project)
    if path.isfile(fpath):
        with open(fpath) as fp:
            nonce = json.load(fp)
    else: nonce = {}
    delta =  time.time() - 86400
    for g in (x for x in gauges if not x in nonce):
        nonce[g] = delta
    return nonce

# Update the nonce.
def update_nonce(project,nonce):
    check_proj(project)
    fpath = 'tmp/projects/{}/nonce.json'.format(project)
    with open(fpath,'w') as fp:
        json.dump(nonce,fp)
