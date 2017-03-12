# -*- coding: utf-8 -*-
"""
This module contains code for creating subclasses of TraitMenu
using information about their options & flags found in a json file.

e.g., see ./data/dmenu_opts.json
"""
import logging as _logging
_logr = _logging.getLogger(__name__)
_logr.addHandler(_logging.NullHandler())

from dynmen.common import Option, Flag
from collections import namedtuple

def _prep_dict(d):
    flag = d['flag']
    d_new = {}
    if not isinstance(flag, str):
        flag = max(flag, key=len)
    d_new['flag'] = flag
    d_new['name'] = flag.lstrip('-').replace('-', '_')
    try:
        d_new['help'] = d['info']
    except KeyError:
        pass
    try:
        d_new['info_text'] = d['arg']
    except KeyError:
        pass
    if d.get('arg', ''):
        d_new['klass'] = Option
    else:
        d_new['klass'] = Flag
    _logr.debug('Transformed option dictionary %r into %r', d, d_new)
    return d_new

NamedDescriptor = namedtuple('NamedDescriptor', 'name descriptor')
def dict_to_descriptor(d):
    d = _prep_dict(d)
    cls = d.pop('klass')
    name = d.pop('name')
    res = NamedDescriptor(name, cls(**d))
    _logr.debug('Created descriptor %r', res)
    return res

class AddOptions(object):
    """
    A class decorator for TraitMenus which
    adds options to the menu
    """
    def __init__(self, *options):
        """Create AddOptions decorator."""
        self.options = options

    def __call__(self, cls):
        for opt in self.options:
            if getattr(cls, opt.name, None) is None:
                setattr(cls, opt.name, opt.descriptor)
                opt.descriptor.class_init(cls, opt.name)
        return cls

def load_options(filepath):
    import json
    with open(filepath, mode='rt') as fp:
        return [dict_to_descriptor(x) for x in json.load(fp)]

