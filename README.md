# egauge

Utilities for logging from eGauge power monitors.

## Purpose

This collection is meant to support remote logging from eGauge
power monitoring devices. It is being developed by Forrest Marshall
on behalf of CSBCD at UH Manoa.

## Usage

This utility is built around the concept of 'projects'.
Each project folder (located in [`tmp/projects/`](./tmp/projects/))
must, at a minimum, contain a `config.json` file, which
dictates what egauges are to be queried, how, if at all,
the data should be reformatted, and what
method(s) of export should be used.  
