#!/usr/bin/env python
from collections import namedtuple
import re

OptTuple = namedtuple('OptTuple', ('flag', 'arg', 'info', 'default', 'dtype'))

options = []
def opt(flag, arg='', info='', default=None, dtype=None):
    info = re.sub('\s+', ' ', info).strip()
    if dtype is not None:
        dtype = dtype.__name__
    options.append(OptTuple(flag, info, arg, default, dtype))

def switch(flag, info=''):
    opt(flag, arg='', info=info, default=False, dtype=bool)

switch('-b', 'dmenu appears at the bottom of the screen.')
switch('-f',
    """dmenu grabs the keyboard before reading stdin.  This is
    faster,  but  will  lock   up  X  until  stdin  reaches
    end-of-file.""")
switch('-i', 'dmenu matches menu items case insensitively.')
opt('-l', 'lines',
    "dmenu lists items vertically,  with the given number of lines.",
    dtype=int,)
opt('-m', 'monitor',
    "dmenu    is   displayed    on   the    monitor   number supplied. Monitor numbers are starting from 0.",
    dtype=int)
opt('-p', 'prompt',
    "defines the prompt  to be displayed to the  left of the input field.",
    dtype=str)

opt('-fn', 'font',
    "defines the font or font set used.")
opt('-nb', 'color',
    "defines  the normal  background color.   #RGB, #RRGGBB, and X color names are supported.")
opt('-nf', 'color', 'defines the normal foreground color.')
opt('-sb', 'color', 'defines the selected background color.')
opt('-sf', 'color', 'defines the selected foreground color.')
switch('-v', 'prints version information to stdout, then exits.')


if __name__ == '__main__':
    import json
    options = [x._asdict() for x in options]
    print(json.dumps(options, indent=2, sort_keys=True))

