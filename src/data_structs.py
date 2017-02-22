#!/usr/bin/env python3
from collections import namedtuple

# Row Tuple
# All the speed and low overhead of a tuple...
# All the explicitness and idiot-proofing of named fields...
Row = namedtuple('row',['node','sensor','unit','timestamp','value'])
