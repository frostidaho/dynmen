#!/usr/bin/env python
import string
import textwrap
import pprint

from dynmen import Menu


fzf = Menu(command=('fzf',))

exampl_inp_dict = vars(string)
exampl_inp_dict = {k:v for k,v in exampl_inp_dict.items() if not k.startswith('_')}

def print_obj(obj, prefix='    '):
    txt = pprint.pformat(obj)
    lines = []
    for line in txt.splitlines():
        line = textwrap.indent(line, prefix)
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

run_n_print(exampl_inp_dict, 'fzf')
run_n_print(exampl_inp_dict, 'fzf.sort')
run_n_print(list(exampl_inp_dict), 'fzf')

