# -*- coding: utf-8 -*-
import subprocess as _sp
from . import ProcStatus

def launch(cmd, fn_input):
    PIPE = _sp.PIPE
    proc = _sp.Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    bstr = fn_input()
    stdout, stderr = proc.communicate(bstr)
    try:
        proc.terminate()
    except ProcessLookupError:
        pass
    return ProcStatus(stdout, stderr, proc.returncode)

