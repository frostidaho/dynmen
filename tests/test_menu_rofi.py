import pytest

integration = pytest.importorskip('integration')

import os

@pytest.fixture(scope='function')
def xctrl():
    xctrl = integration.xcontrol()
    yield xctrl
    try:
        xctrl.proc.terminate()
    except:
        pass

from dynmen.menu import Menu
from time import sleep

def test_simple(xctrl):
    os.environ['DISPLAY'] = xctrl.display_str
    menu = Menu(['rofi', '-dmenu'])
    menu.process_mode = 'futures'
    res = menu(['a', 'b', 'c'])
    sleep(1.0)
    xctrl.type_str('b')
    xctrl.hit_enter()
    out = res.result()
    assert out.selected == 'b'
    assert out.value == None
    

