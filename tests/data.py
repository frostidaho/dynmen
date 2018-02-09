# -*- coding: utf-8 -*-
import json as _json
from collections import OrderedDict as _OrderedDict
import os as _os

_thisdir = _os.path.dirname(__file__)


class MenuData(object):
    _data_files = [
        'data.json',
    ]

    def __init__(self, *args, **kwargs):
        dfiles = [_os.path.join(_thisdir, x) for x in self._data_files]
        for fpath in dfiles:
            with open(fpath, 'rt') as fdata:
                dat = _json.load(fdata)
                for k, v in dat.items():
                    setattr(self, k, v)
        self.people = _OrderedDict(self.people)
