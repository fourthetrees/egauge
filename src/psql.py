#!/usr/bin/env python3
import psycopg2 as psql
from data_structs import Row


def push(data):
    for d,_i in zip(data,range(20)):
        if not isinstance(d,Row):
            raise Exception("Invalid Row Type!")
    exec_push(data)

def exec_push(data):
    cmd = 'INSERT INTO egauge_test (datetime, sensor_id, enduse, value) VALUES (%s, %s, %s, %s)'
    with psql.connect('dbname=frog_uhm user=postgres') as con:
        with con.cursor() as cur:
            cur.executemany(cmd,data)
    con.close()

