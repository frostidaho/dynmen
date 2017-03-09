# -*- coding: utf-8 -*-
import json as _json
from collections import OrderedDict as _OrderedDict

class MenuData(object):
    def __init__(self, *args, **kwargs):
        with open('data.json', 'rb') as fdata:
            dat = _json.load(fdata)

        for k,v in dat.items():
            setattr(self, k, v)

        self.people = _OrderedDict(self.people)


