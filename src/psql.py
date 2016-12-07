#!/usr/bin/env python3
import psycopg2 as psql
from src.data_structs import Row


def push(data):
    for d,_i in zip(data,range(20)):
        if not isinstance(d,Row):
            raise Exception("Invalid Row Type!")
    exec_push(data)

def exec_push(data):
    cmd = 'INSERT INTO egauge_test (datetime, sensor_id, enduse, value) VALUES (to_timestamp(%s), %s, %s, %s)'
    with psql.connect(database='frog_uhm') as con:
        for row in data:
            try:
                with con.cursor() as cur:
                    cur.execute(cmd,row)
                con.commit()
            except psql.IntegrityError:
                con.rollback()
    con.close()

