#!/usr/bin/env python
import re
import subprocess as sp
from itertools import chain
from class_generator import Flag, Option, MenuType, Assignment

def get_outp(*cmd):
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    return stdout.decode()

def man_dmenu():
    return get_outp('man', '-P', 'cat', 'dmenu')

def get_sections(man_page):
    pat = '^(?P<section>[A-Z]+[\sA-Z]*$)'
    secs = list(re.finditer(pat, man_page, flags=re.MULTILINE))
    locs = list(chain(*(x.span() for x in secs)))
    # print(locs)
    d = {}
    
    for sec in secs:
        gdict = sec.groupdict()
        section_name = gdict['section']
        sec_begin = sec.end()
        idxend = locs.index(sec_begin) + 1
        # print('idxend = ', idxend)
        try:
            sec_end = locs[idxend]
            d[section_name] = man_page[sec_begin:sec_end]
        except IndexError:
            d[section_name] = man_page[sec_begin:]

    return d

def build_pattern():
    from collections import OrderedDict
    patterns = OrderedDict()
    patterns['flag'] = '-\w+'
    patterns['arg'] = '\s\w+'
    patterns['info'] = '\s+\w+(.|\n)+'

    patts = OrderedDict()
    for k,v in patterns.items():
        patts[k] = '(?P<{}>'.format(k) + v + ')'

    pat = '^' + patts['flag'] + patts['arg'] + '*' + patts['info']

    pc = re.compile(pat, flags=re.MULTILINE)
    return pc

def parse_options(man_page):
    pc = build_pattern()
    def search_str(txt):
        res = pc.search(txt)
        gdict = res.groupdict()
        # print(gdict)
        d = {}
        for k,v in gdict.items():
            if v is not None:
                d[k] = v.strip().replace('\n', ' ')
            else:
                d[k] = v
        return d

    txt = get_sections(man_page)['OPTIONS']
    opts = re.split('^\n', txt, flags=re.MULTILINE)
    opts = (x.strip() for x in opts if x)
    opts = (search_str(x) for x in opts)
    return list(opts)


def make_attribute(option):
    if option['arg'] is None:
        klass = Flag
    else:
        klass = Option
    flag = option['flag']
    info_text = option['info']
    return klass(flag, info_text=info_text)

if __name__ == '__main__':
    import logging
    logr = logging.getLogger(__name__)
    logr.setLevel(logging.DEBUG)

    opts = parse_options(man_dmenu())
    opts = [make_attribute(x) for x in opts]
    dmenu_src = MenuType('DMenu', *opts)

    try:
        dmenu_src.create_class()
    except:
        logr.exception("Couldn't create DMenu class")

    source = str(dmenu_src)
    try:
        from yapf.yapflib.yapf_api import FormatCode
        source, changed = FormatCode(
            source,
            style_config='pep8',
        )
    except ImportError:
        logr.exception("Couldn't import the yapf code formatter!")

    print(source)



