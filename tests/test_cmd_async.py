import dynmen.cmd.async as dasync
import asyncio


def test_coro_launch():
    inp = b'1\n2\n3\n'
    cmd = ['cat']
    @asyncio.coroutine
    def getinput():
        return inp
    loop = asyncio.get_event_loop()

    out = loop.run_until_complete(dasync._launch(cmd, getinput()))
    assert out.stdout == inp
    assert out.stderr == b''
    assert out.returncode == 0

    out = loop.run_until_complete(dasync.launch(cmd, getinput()))
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

def test_fn_launch():
    inp = b'99\n98\n97\n96'
    cmd = ['cat']
    def getinput():
        return inp

    coro = dasync.launch(cmd, getinput)
    loop = asyncio.get_event_loop()
    out = loop.run_until_complete(coro)
    assert out.stdout == inp
    assert out.stderr == b''
    assert out.returncode == 0

