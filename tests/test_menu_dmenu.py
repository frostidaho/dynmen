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
from time import sleep

MAX_WAIT = 3.0
SPAWN_WAIT = 1.0

@pytest.fixture(scope='function')
def dmenu(xctrl):
    menu = Menu(['dmenu'], process_mode='futures', env={'DISPLAY': xctrl.display_str})
    return menu

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
    dmenu.command.append('-i')
    future = dmenu(['aaa', 'bbb', 'ccc'])
    sleep(SPAWN_WAIT)
    xctrl.type_str('CC')
    xctrl.hit_enter()
    assert_future(future, 'ccc', None)
