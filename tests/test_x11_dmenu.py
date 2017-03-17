import os
import pytest
fixtures = pytest.importorskip('fixtures')
from distutils.spawn import find_executable
exists = find_executable('dmenu')
pytestmark = pytest.mark.skipif(
    not exists,
    reason="dmenu isn't available.",
)

xctrl = fixtures.xctrl
from dynmen.menu import Menu
from dynmen.dmenu import DMenu
from time import sleep

def pytest_generate_tests(metafunc):
    if 'dmenu' in metafunc.fixturenames:
        metafunc.parametrize(
            'dmenu',
            ['Menu', 'DMenu'],
            indirect=True,
        )

MAX_WAIT = 3.0
SPAWN_WAIT = 1.0

@pytest.fixture(scope='function')
def dmenu(request, xctrl):
    if request.param == 'Menu':
        return Menu(['dmenu'], process_mode='futures')
    elif request.param == 'DMenu':
        return DMenu(process_mode='futures')

def assert_future(future, selected, value):
    out = future.result(MAX_WAIT)
    assert out.selected == selected
    assert out.value == value

def test_simple(dmenu, xctrl):
    res = dmenu(['a', 'b', 'c'])
    sleep(SPAWN_WAIT)
    xctrl.type_str('b')
    xctrl.hit_enter()
    assert_future(res, 'b', None)

def test_simple_dict(dmenu, xctrl):
    res = dmenu(dict(zip('abc', [1,2,3])))
    sleep(SPAWN_WAIT)
    xctrl.type_str('c')
    xctrl.hit_enter()
    assert_future(res, 'c', 3)

def test_non_matching_dict(dmenu, xctrl):
    res = dmenu(dict(zip('abc', [1,2,3])))
    sleep(SPAWN_WAIT)
    xctrl.type_str('some other string')
    xctrl.hit_enter()
    assert_future(res, 'some other string', None)

def test_case_insensitive_dict(dmenu, xctrl):
    try:
        dmenu.command.append('-i')
    except AttributeError:
        dmenu.case_insensitive = True
    future = dmenu(['aaa', 'bbb', 'ccc'])
    sleep(SPAWN_WAIT)
    xctrl.type_str('CC')
    xctrl.hit_enter()
    assert_future(future, 'ccc', None)
