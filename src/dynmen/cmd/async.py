# -*- coding: utf-8 -*-
from . import ProcStatus, _to_bytes
import asyncio
import os
from asyncio import subprocess
from collections import namedtuple as _namedtuple


TransPipe = _namedtuple('TransPipe', 'writer write_pipe read_pipe')
@asyncio.coroutine
def get_pipes():
    read_fd, write_fd = os.pipe()
    w_pipe = open(write_fd, 'wb', 0)
    loop = asyncio.get_event_loop()
    w_transport, _ = yield from loop.connect_write_pipe(
        asyncio.Protocol,
        w_pipe,
    )
    r_pipe = open(read_fd, 'rb', 0)
    return TransPipe(w_transport, w_pipe, r_pipe)


@asyncio.coroutine
def _launch(cmd, coro):
    transport, write_pipe, read_pipe = yield from get_pipes()
    proc = yield from asyncio.create_subprocess_exec(
        *cmd,
        stdin=read_pipe,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdin_bytes = yield from coro
    transport.write(stdin_bytes)
    transport.close()
    
    stdout, stderr = yield from proc.communicate()
    retcode = proc.returncode
    write_pipe.close(), read_pipe.close()
    return ProcStatus(stdout, stderr, retcode)


def _build_coro(obj, entry_sep=b''):
    if asyncio.iscoroutine(obj):
        return obj
    elif asyncio.iscoroutinefunction(obj):
        return obj()

    @asyncio.coroutine
    def wrapper(obj):
        try:
            return _to_bytes(obj, entry_sep)
        except TypeError:
            res = yield from wrapper(obj())
            return res

    return wrapper(obj)

@asyncio.coroutine
def launch(cmd, stdin, entry_sep=b''):
    result = yield from _launch(cmd, _build_coro(stdin, entry_sep))
    return result



