from dynmen.cmd import futures

launch = futures.launch

def test_launch_bytes():
    inp = b'sfd8zjzunfzl3'
    inpfn = lambda: inp
    out = launch(['cat'], inpfn)
    out = out.result()
    assert out.stdout == inp
    assert out.stderr == b''
    assert out.returncode == 0

def test_launch_list_of_bytes():
    inp = [b'1', b'2', b'3']
    inpfn = lambda: b'@'.join(inp)
    out = launch(['cat'], inpfn)
    out = out.result()
    assert out.stdout == b'@'.join(inp)
    assert out.stderr == b''
    assert out.returncode == 0

def test_launch_list_of_bytes2():
    inp = [b'4', b'5', b'6']
    entry_sep = b'\n'
    inpfn = lambda: entry_sep.join(inp)
    out = launch(['cat'], inpfn)
    out = out.result()
    assert out.stdout == entry_sep.join(inp)
    assert out.stderr == b''
    assert out.returncode == 0

