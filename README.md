# egauge
  Utilities for logging from eGauge power monitors.

## Purpose
  This collection is meant to support remote logging from eGauge power monitoring devices.  It is being developed by Forrest Marshall on behalf of CSBCD at UH Manoa.

## Basic Usage
  Add all relavent egauges to the `tmp/gauges.json` file (form: `{"gauge_name": gauge_number}`).
  Ensure that the database name and table in `src/psql.py` match the target destination of the sensor data (currently, all data in the `tmp/` folder is treated as unsafe, and as such database name and table are hard-coded in the query script).

  Calling `main.py` will automatically query all gauges in the `gauges.json` file, and save them to the supplied psql table.
  `main.py` will request all data past the value stored in `tmp/nonce.json` for each gauge.
  If no nonce file is found, the past 24 hours worth of data will be requested.
  If all data is successfully added to psql, the nonce file will be updated with the most recent timestamp returned by the query.  IntegrityErrors (violations of primary-key) are silently ignored.
  All other errors cause a rollback, stop all further execution, and are noted in the log file.

  A basic cron-job to launch `main.py` is located in `src/cron/egauge_cron.py`.
  Update the uri string to match your filesystem, and move the file to your desired cron folder.
  Most systems will not execute cron-jobs with special characters in their filenames; reccommend renaming the file to `egauge_cron` (omitting the `.py` extension).

## Development
  Inkeeping with the goal of making egauge querying as painless as possible, future iterations may automatically set up appropriately named psql tables.
  Support for saving to sqlite, csv, and json files may also be worthwhile.

