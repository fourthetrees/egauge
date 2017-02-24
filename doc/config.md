# Configuration

## Basics

The configuration file is core of how program behavior is defined.
Ideally, one should never have to manually modify any other file,
unless one is adding a new feature.

The configuration lives in `tmp/projects/yourproject/config.json`
and, at a minimum need only consist of two fields, `gauges` and
`export_fmt`:

````javascript
{
"gauges" : {
  // One or more gauges declared here.
  "someGauge" : 666,
  ...
}
"export_fmt" : {
  // One or more export methods declared here.
  "csv" : {
    "save-to" : "default",
  }
}
}
````

The `gauges` field may consist of any number of key-value pairs
of the form `gauge-name : gauge-number`.  The gauge number defines
how the egauge api is actually called; the gauge name is stored in the reading
data as an identifier.

The `export_fmt` field declares one or more export methods.  Currently,
the possible formats are `csv` and `psql`.  Options within export method vary,
for example; `csv` has no required arguments, and can be passed as `"csv" : {}`,
however, `psql` requires the `database` and `table` fields to be filled out,
as default values for these cannot be reasonably inferred.

## Advanced

The only advanced configuration feature which is currently available is the
`mapping` field.  The `mapping` field allows for the renaming, reordering, and
removal of columns, as well as the substitution of various values, and the
addition of new derivative fields.  See [`mapping.md`](./mapping.md) for
more information on setup and use of the `mapping` field.
