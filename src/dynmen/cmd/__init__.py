# -*- coding: utf-8 -*-
from collections import namedtuple as _namedtuple

ProcStatus = _namedtuple('ProcStatus', 'stdout stderr returncode')


def _to_bytes(obj, entry_sep=b''):
    if isinstance(obj, bytes):
        return obj
    return entry_sep.join(obj)
