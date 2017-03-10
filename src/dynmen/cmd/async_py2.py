# -*- coding: utf-8 -*-
from . import ProcStatus
import trollius as asyncio
from trollius import From, Return
import os
from trollius import subprocess
from collections import namedtuple as _namedtuple


TransPipe = _namedtuple('TransPipe', 'writer write_pipe read_pipe')
@asyncio.coroutine
def get_pipes():
    read_fd, write_fd = os.pipe()
    w_pipe = open(write_fd, 'wb', 0)
    loop = asyncio.get_event_loop()
    w_transport, _ = yield From(loop.connect_write_pipe(
        asyncio.Protocol,
        w_pipe,
    ))
    r_pipe = open(read_fd, 'rb', 0)
    raise Return(TransPipe(w_transport, w_pipe, r_pipe))


@asyncio.coroutine
def _launch(cmd, coro):
    transport, write_pipe, read_pipe = yield From(get_pipes())
    cmdgen = asyncio.create_subprocess_exec(*cmd, stdin=read_pipe,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc = yield From(cmdgen)

    stdin_bytes = yield From(coro)
    transport.write(stdin_bytes)
    transport.close()
    
    stdout, stderr = yield From(proc.communicate())
    retcode = proc.returncode
    write_pipe.close(), read_pipe.close()
    raise Return(ProcStatus(stdout, stderr, retcode))


def _build_coro(obj, *args):
    if asyncio.iscoroutine(obj):
        return obj
    elif asyncio.iscoroutinefunction(obj):
        return obj(*args)

    @asyncio.coroutine
    def wrapper(obj, *args):
        return obj(*args)

    return wrapper(obj, *args)

@asyncio.coroutine
def launch(cmd, fn_input, fn_transform_res=None):
    result = yield From(_launch(cmd, _build_coro(fn_input)))
    if fn_transform_res is None:
        raise Return(result)
    else:
        result = yield From(_build_coro(fn_transform_res, result))
    raise Return(result)



