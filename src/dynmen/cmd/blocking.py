# -*- coding: utf-8 -*-
import subprocess as _sp
from . import ProcStatus
try:
    ProcessLookupError
except NameError:               # python2 compatibility
    ProcessLookupError = OSError


def launch(cmd, fn_input, fn_transform_res=None, **kw):
    PIPE = _sp.PIPE
    proc = _sp.Popen(cmd, stdout=PIPE, stdin=PIPE, **kw)
    bstr = fn_input()
    stdout, stderr = proc.communicate(bstr)
    try:
        proc.terminate()
    except ProcessLookupError:
        pass
    result = ProcStatus(stdout, stderr, proc.returncode)
    if fn_transform_res is None:
        return result
    transformed = fn_transform_res(result)
    return transformed
