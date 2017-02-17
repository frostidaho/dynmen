# -*- coding: utf-8 -*-
"""
This module contains code for creating subclasses of TraitMenu
using information about their options & flags found in a json file.

e.g., see ./data/dmenu_opts.json
"""
from dynmen.common import (
    Option as _Option,
    Flag as _Flag,
)

def make_option(**kws):
    """
    Given a dict kws with keys like {'flag', 'default', 'dtype', ...}

    Return a dynmen.common.Option or dynmen.common.Flag descriptor
    """
    dtypes = {'bool': bool, 'float': float, 'int': int, 'str': str}
    flag_args = {'name', 'default', 'info', 'flag'}
    kws['dtype'] = dtypes.get(kws.get('dtype'), None)
    kws = {k:v for k,v in kws.items() if v is not None}
    if not isinstance(kws['flag'], str):
        kws['flag'] = max(kws['flag'], key=len)
    kws['name'] = kws['flag'].lstrip('-').replace('-', '_')

    flag_args = flag_args & kws.keys()
    if (kws.get('dtype') is bool) or (not kws.get('arg')):
        return _Flag(**{k:kws[k] for k in flag_args})
    if 'dtype' in kws:
        flag_args.add('dtype')
    return _Option(**{k:kws[k] for k in flag_args})


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
                setattr(cls, opt.name, opt)
        return cls

def load_options(filepath):
    import json
    with open(filepath, mode='rt') as fp:
        return [make_option(**x) for x in json.load(fp)]

