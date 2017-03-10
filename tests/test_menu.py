import pytest
try:
    import asyncio
    all_modes = ('blocking', 'futures', 'async')
except ImportError:
    all_modes = ('blocking', 'futures')

from dynmen.menu import Menu, MenuError
from traitlets import TraitError

import sys
import logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

@pytest.fixture(scope='module')
def menudata():
    from data import MenuData
    return MenuData()

def test_simple_dict(menudata):
    d_people = menudata.people
    person = list(d_people)[13]
    m = Menu(['grep', person])
    result = m(d_people)
    assert result.selected == person
    assert result.value == d_people[person]

def test_cmd_error():
    m = Menu(['grep', r'\('])
    with pytest.raises(MenuError):
        result = m([])

def test_init():
    cmd = ['cat']
    m = Menu(cmd)
    assert m.command == cmd
    m.process_mode = 'futures'
    assert m.process_mode == 'futures'
    with pytest.raises(TraitError):
        m.process_mode = 37
    cmd = ['grep']
    m.command = cmd
    assert m.command == cmd
    with pytest.raises(TraitError):
        m.command = 'some-string'

noval = ('noval',)

def run_blocking_mode(menu, entries, exceptions):
    menu.process_mode = 'blocking'
    if exceptions is not None:
        with pytest.raises(exceptions):
            res = menu(entries)
        return noval
    else:
        res = menu(entries)
        return res

def run_futures_mode(menu, entries, exceptions):
    menu.process_mode = 'futures'
    future = menu(entries)
    if exceptions is not None:
        with pytest.raises(exceptions):
            res = future.result()
        return noval
    else:
        return future.result()

def run_async_mode(menu, entries, exceptions):
    menu.process_mode = 'async'
    loop = asyncio.get_event_loop()
    if exceptions is not None:
        with pytest.raises(exceptions):
            res = loop.run_until_complete(menu(entries))
        return noval
    else:
        res = loop.run_until_complete(menu(entries))
        return res

def run_all_modes(menu, entries, selected=noval, value=noval, exceptions=None,
                  modes=all_modes):
                  # modes=(run_blocking_mode, run_futures_mode, run_async_mode)):
    def check_res(res):
        if selected != noval:
            assert res.selected == selected
        if value != noval:
            assert res.value == value
        return res
        
    modes = [globals()['run_{}_mode'.format(x)] for x in modes]
    for fn in modes:
        res = fn(menu, entries, exceptions)
        if res != noval:
            check_res(res)
    

def test_simple_dict_all(menudata):
    d_people = menudata.people
    person = list(d_people)[13]
    menu = Menu(['grep', person])
    run_all_modes(
        menu,
        d_people,
        selected=person,
        value=d_people[person],
    )

def test_cmd_error_all():
    menu = Menu(['grep', r'\('])
    run_all_modes(
        menu,
        [],
        exceptions=MenuError,
    )

def test_list_all(menudata):
    lpeople = list(menudata.people)
    person = lpeople[27]
    menu = Menu(['grep', person])
    run_all_modes(
        menu,
        lpeople,
        selected=person,
        value=None,
    )

def test_generator_all():
    selected = '41'
    menu = Menu(['grep', selected])
    # modes = [
    #     run_blocking_mode,
    #     run_futures_mode,
    #     run_async_mode,
    # ]
    for mode in all_modes:
        run_all_modes(
            menu,
            (str(x) for x in range(100)),
            selected=selected,
            value=None,
            modes=(mode,),
        )

def test_string_all():
    entries = '\n'.join('123456789')
    selected = '4'
    menu = Menu(['grep', selected])
    run_all_modes(
        menu,
        entries,
        selected=selected,
        value=None,
    )

def test_string_all2():
    entries = '\n'.join('123456789')
    menu = Menu(['cat'])
    run_all_modes(
        menu,
        entries,
        selected=entries,
        value=None,
    )

def test_convert_entries_bytes():
    menu = Menu(['cat'])
    entries = b'987654321'
    run_all_modes(menu, entries, selected=entries.decode('utf8'), value=None)

def test_entry_sep():
    menu = Menu(['cat'], entry_sep='@')
    entries = list('987654321')
    run_all_modes(menu, entries, selected='@'.join(entries), value=None)

def test_entry_sep2():
    menu = Menu(['cat'])
    menu.entry_sep = '#'
    entries = list('987654321')
    run_all_modes(menu, entries, selected='#'.join(entries), value=None)

def test_entry_sep3():
    menu = Menu(['cat'])
    entries = list('987654321')
    res = menu(entries, entry_sep='!')
    assert res.selected == '!'.join(entries)

def test_entry_list_bytes():
    menu = Menu(['cat'])
    entries = [b'1', b'2', b'33']
    res = menu(entries, entry_sep='!')
    assert res.selected == b'!'.join(entries).decode('utf8')

def test_menu_equality():
    menu = Menu(['cat'])
    menu2 = Menu(['cat'])
    hash_menu2 = hash(menu2)
    assert menu == menu2
    assert hash(menu) == hash_menu2
    menu.entry_sep = '@\n'
    assert menu != menu2
    assert hash(menu) != hash_menu2

def test_menu_repr():
    menu = Menu(['cat'])
    rmenu = repr(menu)
    assert eval(rmenu) == Menu(['cat'])

