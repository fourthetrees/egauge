#!/usr/bin/env python3
import psycopg2 as psql
from src.data_structs import Row
from src.errlog import fmterr

# Main save-to-psql entry point.
def to_psql(data,project,psql_config):
    db  = psql_config['database']
    tbl = psql_config['table']
    fields = data[0]._fields
    if 'type-conversions' in psql_config:
        ins = custom_ins(fields,psql_config['type-conversions'])
    else: ins = ','.join(['%s'] * len(fields))
    cmd = 'INSERT INTO {} VALUES ({})'.format(tbl,ins)
    errs = exec_push(data,cmd,db)
    if errs: fmterr(project,data,txt='psqlerr')

# Actually push the stuff
def exec_push(data,cmd,db):
    errs = []
    with psql.connect(database=db) as con:
        for row in data:
            try:
                with con.cursor() as cur:
                    cur.execute(cmd,row)
                con.commit()
            except psql.IntegrityError:
                errs.append(row)
                con.rollback()
    con.close()
    return errs

# Generate a custom insertion string
# for psql conversion commands.
def custom_ins(fields,insmap):
    inserts = {
        'default' : '%s',
        'to-timestamp' : 'to_timestamp(%s)'
    }
    for i in insmap:
        if i not in fields:
            raise Exception('unrecognized field: {}'.format(i))
        if insmap[i] not in inserts:
            raise Exception('unrecognized type conversion: {}'.format(insmap[i]))
    ins = []
    for f in fields:
        if f in insmap:
            ins.append(inserts[insmap[f]])
        else: ins.append(inserts['default'])
    return ','.join(ins)
