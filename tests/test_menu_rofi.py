import pytest

integration = pytest.importorskip('integration')

import os
n_display = integration.start_xephyr()
xctrl = integration.xcontrol(n_display)
os.environ['DISPLAY'] = ':{:d}'.format(n_display)

from dynmen.menu import Menu
from time import sleep


def test_simple():
    menu = Menu(['rofi', '-dmenu'])
    menu.process_mode = 'futures'
    res = menu(['a', 'b', 'c'])
    sleep(1.0)
    xctrl.type_str('b')
    xctrl.hit_enter()
    out = res.result()
    assert out.selected == 'b'
    assert out.value == None

