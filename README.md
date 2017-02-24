# egauge

Utility for logging & reformatting data from eGauge power monitors.

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
method(s) of export should be used.  See the
[`doc/config.md`](./doc/config.md) file for an
explanation of how to construct a configuration file
from scratch.

When a new project is begun, one may optionally add
a `nonce.json` file to the project folder as well.
This file is a simple key-value pair consisting of
gauge names (as specified in the configuration file)
and unix timestamps. The nonce file determines how
much historical data is scraped, and is updated to
the most recent set of values received upon a successful
scrape. If no nonce file is found, the previous 24 hours
of data will be retrieved, and a new nonce based upon
the received readings will be generated.

In addition to the `projects` folder, two other folders,
`errors` and `outputs`, may be generated within [`tmp/`](./tmp/).
These folders, as their names imply, are the default
destination of error logs and file outputs respectively.
Ideally, this inkeeping with the project-based model,
all files generated will appear in an appropriately named
project folder, e.g.; a csv of data from the `net-zero-solar`
project would appear as `tmp/outputs/net-zero-solar/some_output.csv`.

## Ongoing Development

The next phase of development will include a more comprehensive
way to register active projects (currently a hard-coded list in
[`main.py`](./main.py)), and improved helpers for registering
the utility as a cron job.  Expanded commenting is also in
the pipes, as some of the more hastily written sections of
the code base contain only bare-bones descriptions of
their functionality and rationale.

## Contribution

Pull requests welcome!
