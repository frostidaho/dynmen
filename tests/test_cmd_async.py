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

def test_list_of_bytes_launch():
    inp = [b'1', b'2', b'33']
    cmd = ['cat']

    coro = dasync.launch(cmd, inp)
    loop = asyncio.get_event_loop()
    out = loop.run_until_complete(coro)
    assert out.stdout == b''.join(inp)
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

