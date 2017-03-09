import subprocess as _sp
from . import ProcStatus, _to_bytes

def launch(cmd, stdin):
    PIPE = _sp.PIPE
    proc = _sp.Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    bstr = _to_bytes(stdin)
    stdout, stderr = proc.communicate(bstr)
    try:
        p.terminate()
    except ProcessLookupError:
        pass
    return ProcStatus(stdout, stderr, p.returncode)

