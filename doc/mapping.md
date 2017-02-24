# Mapping

## Overview

The `mapping` field allows for the renaming, reordering, and
removal of columns, as well as the substitution of various values,
and the addition of new derivative fields.

Usage of the `mapping` field is and advanced feature, but with a
little patience, it can allow for the automation of very powerful
data reformatting.  The `mapping` configuration option currently
consists of three sub-options, `content`, `fields`, and
`generated-fields`, each of which is explained in detail below.

## Field Mapping

The most straightforward mapping option is the `fields` option.
This option allows the the explicit renaming and reordering of
one or more of the default data fields.  By default, data is
passed as named tuples with the structure:

````markdown
| node | sensor | unit | timestamp | value |
| ---- | ------ | ---- | --------- | ----- |
| ...  | ...    | ...  | ...       | ...   |
````

This is an extremely general structure designed to easily encode
data from a variety of loggers, but it is rarely the ideal form
for a given application.  We can rename and restructure if by
adding a sub-option within `fields` corresponding to one or more
of the default field names.  Each declaration must contain a
`name` field and an `index` field.  If, for example, we would like
the first column of our new mapping to contain the timestamp and be
named `time_of_reading`, we would declare it like so:

````javascript
"timestamp" : {
  "name"  : "time_of_reading",
  "index" : 0
}
````

## Content Mapping

The `content` mapping option allows for explicit replacement of values
within a field.  This is mostly useful for a field which contains
categorical data (names, units, etc...).  Mappings for a given field
are declared within a configuration field of the same name.  Content
mapping occurs before field mapping, and therefore will not conflict
with any renaming.

Each content mapping field consists of two sub-fields; a required
`map` field which actually contains the value mapping, and an
optional `ignore` field which lists values to ignore.  Any value
encountered which is not listed in `map` or `ignore` is treated
as erroneous, and logged to a csv file in `tmp/errors/project-name/...`.
The `map` field can contain any numer of key-value pairs, with the
key being an expected value, and the value being the desired replacement.
Say, for example, that we wanted to have all units in `kW` be replaced
by `fahrenheit`, and all units in `kWh` go silently unrecorded.  We could
achieve this like so:

````javascript
"unit" : {
  "map" : {
    "kW" : "fahrenheit"
  }
  "ignore" : [
    "kWh"
  ]
} // Some people just want to watch the world burn...
````


## Generated-Field Mapping

TODO
