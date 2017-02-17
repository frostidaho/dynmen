#!/usr/bin/env python3
from parsimonious.grammar import Grammar
import subprocess as sp
import re

def get_outp(*cmd):
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    return stdout.decode()

def get_option_strings():
    rofi_help = get_outp('rofi', '-h')
    begin_str = 'rofi [-options ...]'
    idx_begin = rofi_help.find(begin_str)
    assert idx_begin != -1
    idx_begin += len(begin_str)
    idx_end = re.search('^Monitor layout:$', rofi_help, flags=re.MULTILINE).start()

    rofi_help = rofi_help[idx_begin:idx_end]
    lines = [x for x in rofi_help.splitlines() if x and x.startswith('\t')]

    rofi_help = '\n'.join(lines)
    rofi_help = rofi_help.replace('\n\t\t', ' @@@ ')
    opts = [x.lstrip('\t') for x in rofi_help.splitlines()]
    opts2 = []
    for opt in opts:
        if opt.startswith('-[no-]'):
            opt_pos = opt.replace('-[no-]', '-', 1)
            opt_neg = opt.replace('-[no-]', '-no-', 1)
            opts2.append(opt_pos)
            opts2.append(opt_neg)
        else:
            opts2.append(opt)
    return opts2

opts = get_option_strings()

grammar = Grammar(
    r"""
    all = option / switch
    switch = flags info
    option = flags arg info
    flags = ~"^" flag otherflag?
    otherflag = "," flag
    flag = ~"-{1,2}[-\w]+"
    arg = ~"\s*\[\w+\]\s*"
    info = ~".*$"
    """
)

def get_parsed_keys(node, *keys):
    for child in node.children:
        yield from get_parsed_keys(child, *keys)
    if node.expr_name in keys:
        yield (node.expr_name, node.text)

def parse_opt(opt):
    parsed = grammar.parse(opt)
    keys = list(get_parsed_keys(parsed, 'flag', 'arg', 'info'))
    from collections import defaultdict
    d = defaultdict(list)
    for k,v in keys:
        d[k].append(v.strip())

    d2 = {}
    for k,v in d.items():
        if k != 'flag':
            v = ' '.join(v)
        elif len(v) == 1:
            v = v[0]
        d2[k] = v
    return d2

opts = [parse_opt(x) for x in opts]
import json
print(json.dumps(opts, indent=2, sort_keys=True))


