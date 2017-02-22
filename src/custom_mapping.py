#!/usr/bin/env python3
from collections import namedtuple
from src.data_structs import Row
import time

# primary entry point for performing
# a custom mapping.
def fmt_mapping(data,mapping):
    maperr = []
    if 'content' in mapping:
        data,err = map_content(data,mapping['content'])
        maperr += err
    if 'fields' in mapping:
        data = map_fields(data,mapping['fields'])
    if 'generated-fields' in mapping:
        data = gen_fields(data,mapping['generated-fields'])
    if maperr:
        print('mapping failed for {} out of {} rows'
            .format(len(maperr),len(data) + len(maperr)))
        fmterr(project,maperr)
    return data

# map the content of one or more fields
# to some new set of values.  Any rows
# containing values not in valmap are
# returned in a separate maperr list.
# ie; partial mappings for a given
# column are not allowed.  This is based
# on the assumption that mappings may change
# datatype (eg; string to int).
def map_content(data,valmap):
    valmap = { k.lower() : valmap[k] for k in valmap }
    dfields = data[0]._fields
    maperr = []
    mapped = []
    for field in valmap:
        if field not in dfields:
            raise Exception('invalid mapping: {}'.format(field))
        index = dfields.index(field)
        if 'ignore' in valmap[field]:
            ignore = [i.lower() for i in valmap[field]['ignore']]
        else: ignore = []
        fmap = valmap[field]['map']
        fmap = { k.lower() : fmap[k] for k in fmap }
        for d in data:
            r = [f for f in d]
            val = r[index]
            if val in fmap:
                r[index] = fmap[val]
                mapped.append(Row(*r))
            else:
                if val in ignore: continue
                else: maperr.append(Row(*r))
        data = [ r for r in mapped ]
        mapped = []
    return data,maperr


# Maps default fields to a new field mapping.
# Accepts field map of form:
# ````
# {
# "defaultname" : {
#       "name" : "newname"
#       "index" : n // some new position
#   }
# }
# ````
# Any fields not in mapping are dropped.
def map_fields(data,fieldmap):
    fieldmap = { k.lower() : fieldmap[k] for k in fieldmap }
    dfields  = data[0]._fields
    indexmap = []
    namemap  = []
    for di,df in enumerate(dfields):
        if not df in fieldmap: continue
        mf = fieldmap[df]['name']
        mi = fieldmap[df]['index']
        indexmap.append((mi,di))
        namemap.append((mi,mf))
    sbi = lambda i: i[0]
    foi = lambda l: [x[1] for x in l]
    indexmap = foi(sorted(indexmap,key=sbi))
    namemap  = foi(sorted(namemap,key=sbi))
    fmtrow   = namedtuple('fmtrow', namemap)
    fmtdata  = []
    for d in data:
        row = []
        for i in indexmap:
            row.append(d[i])
        fmtdata.append(fmtrow(*row))
    return fmtdata


# Add one or more generated fields
def gen_fields(data,gfields):
    generators = { "upload-time" : upload_time() }
    errgf = [f for f in gfields if not f in generators]
    if errgf:
        raise Exception('invalid generated-field(s): {}'.format(errgf))
    dfields = list(data[0]._fields)
    gindex = []
    # populate gindex w/ (index,name,generator)
    for g in gfields:
        gi = []
        gi.append(gfields[g]['index'])
        gi.append(gfields[g]['name'])
        gi.append(g)
        gindex.append(tuple(gi))
    sbi = lambda i: i[0]
    foi = lambda l: [ x[1] for x in l ]
    fog = lambda l: [ x[2] for x in l ]
    gindex    = sorted(gindex,key=lambda i: i[0])
    nameindex = foi(gindex)
    genindex  = fog(gindex)
    row_new   = namedtuple('row',dfields + nameindex)
    data_new  = []
    for d in data:
        gf = [ generators[g]() for g in genindex ]
        r  = list(d) + gf
        data_new.append(row_new(*r))
    return data_new


# Returns generator for the
# "uplad-time" generated field.
def upload_time():
    t = time.time()
    return lambda : t
