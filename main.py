#!/usr/bin/env python3
from src.egauge import query_gauges
from src.custom_mapping import fmt_mapping
from src.to_psql import to_psql
from src.to_csv import to_csv
from src.projects import get_params, update_nonce
from src.errlog import mklog
from os.path import dirname
import os
import time
import json

# RunnnnN!!!
def run(project):
    os.chdir(dirname(__file__))
    config,nonce= get_params(project)
    print('querying gauges...')
    data,nonce_new = query_gauges(config["gauges"],nonce)
    handle_data(data,config,project)
    update_nonce(project,nonce_new)

# Do something with the data.
def handle_data(data,config,project):
    if 'mapping' in config:
        print('reformatting data...')
        data = fmt_mapping(data,config['mapping'])
    if not data:
        print('no data valid data... skipping save step.')
        return
    if not 'export_fmt' in config:
        raise Exception('no export format specified for {}!'.format(project))
    export_config = { k.lower() : config['export_fmt'][k]
                    for k in config['export_fmt']      }
    for k in export_config:
        if k == 'csv':
            print('saving {} rows to csv...'.format(len(data)))
            to_csv(data,project,export_config['csv'])
        elif k == 'psql':
            print('saving {} rows to psql...'.format(len(data)))
            to_psql(data,project,export_config['psql'])
        else:
            raise Exception('unrecognized export format: {}'.format(k))

def Main():
    active_projects = ['maui-smart-grid']
    for proj in active_projects:
        # temp uncaugh for debug:
        run(proj)
        '''
        try:
            run(proj)
        except Exception as err:
            print(err)
            mklog(proj,err)
        '''
if __name__ == '__main__':
    Main()
