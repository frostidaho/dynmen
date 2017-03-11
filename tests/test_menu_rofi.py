import pytest
fixtures = pytest.importorskip('fixtures')
from distutils.spawn import find_executable
exists = find_executable('rofi')
pytestmark = pytest.mark.skipif(
    not exists,
    reason="Rofi isn't available.",
)

import os
from dynmen.menu import Menu
from time import sleep
xctrl = fixtures.xctrl


MAX_WAIT = 3.0
@pytest.fixture(scope='function')
def rofi_menu(xctrl):
    os.environ['DISPLAY'] = xctrl.display_str
    menu = Menu(['rofi', '-dmenu'], process_mode='futures')
    return menu

def test_simple(rofi_menu, xctrl):
    menu = rofi_menu
    res = menu(['a', 'b', 'c'])
    sleep(1.0)
    xctrl.type_str('b')
    xctrl.hit_enter()
    out = res.result(MAX_WAIT)
    assert out.selected == 'b'
    assert out.value == None

def test_non_matching(rofi_menu, xctrl):
    menu = rofi_menu
    res = menu(['a', 'b', 'c'])
    sleep(1.0)
    xctrl.type_str('asdfasdf')
    xctrl.hit_enter()
    out = res.result(MAX_WAIT)
    assert out.selected == 'asdfasdf'
    assert out.value == None
    
def test_case_sensitive(rofi_menu, xctrl):
    menu = rofi_menu
    res = menu(['a', 'b', 'c'])
    sleep(1.0)
    xctrl.type_str('C')
    xctrl.hit_enter()
    out = res.result(MAX_WAIT)
    assert out.selected == 'C'
    assert out.value == None

def test_case_insensitive(rofi_menu, xctrl):
    menu = rofi_menu
    menu.command.append('-i')
    res = menu(['a', 'b', 'c'])
    sleep(1.0)
    xctrl.type_str('C')
    xctrl.hit_enter()
    out = res.result(MAX_WAIT)
    assert out.selected == 'c'
    assert out.value == None
