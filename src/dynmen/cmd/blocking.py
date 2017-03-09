# -*- coding: utf-8 -*-
import subprocess as _sp
from . import ProcStatus, _to_bytes

def launch(cmd, stdin, entry_sep=b''):
    PIPE = _sp.PIPE
    proc = _sp.Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    bstr = _to_bytes(stdin, entry_sep)
    stdout, stderr = proc.communicate(bstr)
    try:
        proc.terminate()
    except ProcessLookupError:
        pass
    return ProcStatus(stdout, stderr, proc.returncode)

