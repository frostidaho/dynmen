from dynmen.cmd import blocking
from data import MenuData

launch = blocking.launch

def cat_identity(input_fn, stdout):
    out = launch(['cat'], input_fn)
    assert out.stdout == stdout
    assert out.stderr == b''
    assert out.returncode == 0

def test_launch_bytes():
    inp = b'sfd8zjzunfzl3'
    inpfn = lambda: inp
    cat_identity(inpfn, inp)

def test_launch_list_of_bytes():
    inp = [b'1', b'2', b'3']
    inpfn = lambda: b'@'.join(inp)
    cat_identity(inpfn, b'@'.join(inp))

def test_launch_list_of_bytes2():
    inp = [b'4', b'5', b'6']
    entry_sep = b'\n'
    inpfn = lambda: entry_sep.join(inp)
    cat_identity(inpfn, entry_sep.join(inp))

def test_transform_res():
    md = MenuData()
    lpeople = list(md.people)
    people_txt = '\n'.join(lpeople)
    inpfn = lambda: people_txt.encode()
    cat_identity(inpfn, people_txt.encode())

    person = lpeople[10]
    out = launch(['grep', person], inpfn)
    assert out.stdout.startswith(person.encode())
    out2 = out.stdout.decode().strip()
    assert out2 == person

    person = lpeople[23]
    out = launch(['grep', person], inpfn, lambda x: x.stdout.decode())
    assert out == person + '\n'
    assert md.people[person] == md.people[out.rstrip()]
