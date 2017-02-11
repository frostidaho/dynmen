#!/usr/bin/env python
# This example shows the usage of how to use the Menu() class with rofi.
# Make a Menu() instance by passing a sequence containing your
# menu's command and its corresponding flags & options.
# e.g., rofi = Menu(command=('rofi', '-fullscreen', '-dmenu', '-i'))
# The instance of Menu() is callable and can be given a sequence or a mapping.
from __future__ import print_function
import string
import textwrap
import pprint

from dynmen import Menu


rofi = Menu(command=('rofi', '-fullscreen', '-dmenu', '-i'))

exampl_inp_dict = vars(string)
exampl_inp_dict = {k:v for k,v in exampl_inp_dict.items() if not k.startswith('_')}

def print_obj(obj, prefix='    '):
    txt = pprint.pformat(obj)
    lines = []
    for line in txt.splitlines():
        line = textwrap.fill(line, width=160, initial_indent=prefix, subsequent_indent=prefix)
        lines.append(line)
    print('\n'.join(lines))

def run_n_print(entries, fn_str):
    fn = globals()[fn_str.split('.')[0]]
    for attr in fn_str.split('.')[1:]:
        fn = getattr(fn, attr)
    print("\nLAUNCHING '{}' with -".format(fn_str))
    print_obj(entries)
    output = fn(entries)
    print('OUTPUT IS -')
    print_obj(output)
    return output

run_n_print(exampl_inp_dict, 'rofi')
run_n_print(exampl_inp_dict, 'rofi.sort')
run_n_print(list(exampl_inp_dict), 'rofi')

