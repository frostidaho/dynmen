# -*- coding: utf-8 -*-
import subprocess as _sp
from . import ProcStatus

def launch(cmd, fn_input, fn_transform_res=None):
    PIPE = _sp.PIPE
    proc = _sp.Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    bstr = fn_input()
    stdout, stderr = proc.communicate(bstr)
    try:
        proc.terminate()
    except ProcessLookupError:
        pass
    result = ProcStatus(stdout, stderr, proc.returncode)
    if fn_transform_res is None:
        return result
    return fn_transform_res(result)

