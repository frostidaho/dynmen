import os
import pytest
fixtures = pytest.importorskip('fixtures')
xctrl = fixtures.xctrl
from dynmen.menu import Menu
from time import sleep


MAX_WAIT = 3.0

@pytest.fixture(scope='function')
def dmenu_menu(xctrl):
    os.environ['DISPLAY'] = xctrl.display_str
    menu = Menu(['dmenu'], process_mode='futures')
    return menu

def test_simple(dmenu_menu, xctrl):
    menu = dmenu_menu
    res = menu(['a', 'b', 'c'])
    sleep(1.0)
    xctrl.type_str('b')
    xctrl.hit_enter()
    out = res.result(MAX_WAIT)
    assert out.selected == 'b'
    assert out.value == None


