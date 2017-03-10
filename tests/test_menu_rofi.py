import pytest

integration = pytest.importorskip('integration')
from dynmen.menu import Menu
from time import sleep

def test_simple():
    menu = Menu(['rofi', '-dmenu'])
    menu.process_mode = 'futures'
    res = menu(['a', 'b', 'c'])
    sleep(1.0)
    integration.type_str('b')
    integration.hit_enter()
    out = res.result()
    assert out.selected == 'b'
    assert out.value == None

