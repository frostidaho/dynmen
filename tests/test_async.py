import dynmen.async as dasync
import asyncio


def test_coro_launch():
    inp = b'1\n2\n3\n'
    cmd = ['cat']
    @asyncio.coroutine
    def getinput():
        return inp
    coro = dasync._launch(cmd, getinput())
    loop = asyncio.get_event_loop()
    out = loop.run_until_complete(coro)
    assert out.stdout == inp
    assert out.stderr == b''
    assert out.returncode == 0

def test_bytes_launch():
    inp = b'4\n5\n6\n'
    cmd = ['cat']
    coro = dasync.launch(cmd, inp)
    loop = asyncio.get_event_loop()
    out = loop.run_until_complete(coro)
    assert out.stdout == inp
    assert out.stderr == b''
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
    assert out.stderr == b''
    assert out.returncode == 0

