# -*- coding: utf-8 -*-
import pytest
import sys
pytestmark = pytest.mark.skipif(sys.version_info < (3, 0), reason='needs python3')
try:
    import asyncio
    import dynmen.cmd.async as dasync
except ImportError:
    pass

from data import MenuData


def launch(*args, **kwargs):
    loop = asyncio.get_event_loop()
    coro = dasync.launch(*args, **kwargs)
    return loop.run_until_complete(coro)


def test_coro_launch():
    inp = b'1\n2\n3\n'
    cmd = ['cat']

    @asyncio.coroutine
    def getinput():
        return inp
    loop = asyncio.get_event_loop()

    out = loop.run_until_complete(dasync._launch(cmd, getinput()))
    assert out.stdout == inp
    assert out.stderr is None
    assert out.returncode == 0

    out = loop.run_until_complete(dasync.launch(cmd, getinput()))
    assert out.stdout == inp
    assert out.stderr is None
    assert out.returncode == 0


def test_coro_fn_launch():
    inp = b'7\n9000\n22\n\n'
    cmd = ['cat']

    @asyncio.coroutine
    def getinput():
        return inp
    coro = dasync.launch(cmd, getinput)
    loop = asyncio.get_event_loop()
    out = loop.run_until_complete(coro)
    assert out.stdout == inp
    assert out.stderr is None
    assert out.returncode == 0


def test_fn_launch():
    inp = b'99\n98\n97\n96'
    cmd = ['cat']

    def getinput():
        return inp

    coro = dasync.launch(cmd, getinput)
    loop = asyncio.get_event_loop()
    out = loop.run_until_complete(coro)
    assert out.stdout == inp
    assert out.stderr is None
    assert out.returncode == 0


def test_coro_transform_res():
    md = MenuData()
    lpeople = list(md.people)

    @asyncio.coroutine
    def inpfn():
        x = '\n'.join(lpeople)
        return x.encode()

    out = launch(['cat'], inpfn)
    assert out.stdout == '\n'.join(lpeople).encode()

    @asyncio.coroutine
    def trfn(result):
        return result.stdout.decode()

    out = launch(['cat'], inpfn, trfn)
    assert out == '\n'.join(lpeople)


def test_fn_transform_res():
    md = MenuData()
    lpeople = list(md.people)

    @asyncio.coroutine
    def inpfn():
        x = '\n'.join(lpeople)
        return x.encode()

    def trfn(result):
        return result.stdout.decode()

    out = launch(['cat'], inpfn, trfn)
    assert out == '\n'.join(lpeople)
