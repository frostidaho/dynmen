# -*- coding: utf-8 -*-
from dynmen.cmd import blocking
from data import MenuData

launch = blocking.launch


def cat_identity(input_fn, stdout):
    out = launch(['cat'], input_fn)
    assert out.stdout == stdout
    assert out.stderr is None
    assert out.returncode == 0


def test_launch_bytes():
    inp = b'sfd8zjzunfzl3'

    def inpfn(): return inp
    cat_identity(inpfn, inp)


def test_launch_list_of_bytes():
    inp = [b'1', b'2', b'3']

    def inpfn(): return b'@'.join(inp)
    cat_identity(inpfn, b'@'.join(inp))


def test_launch_list_of_bytes2():
    inp = [b'4', b'5', b'6']
    entry_sep = b'\n'

    def inpfn(): return entry_sep.join(inp)
    cat_identity(inpfn, entry_sep.join(inp))


def test_transform_res():
    md = MenuData()
    lpeople = list(md.people)
    people_txt = u'\n'.join(lpeople)

    def inpfn(): return people_txt.encode('utf8')
    cat_identity(inpfn, people_txt.encode('utf8'))

    person = lpeople[10]
    out = launch(['grep', person], inpfn)
    assert out.stdout.startswith(person.encode())
    out2 = out.stdout.decode().strip()
    assert out2 == person

    person = lpeople[23]
    out = launch(['grep', person], inpfn, lambda x: x.stdout.decode())
    assert out == person + u'\n'
    assert md.people[person] == md.people[out.rstrip()]
