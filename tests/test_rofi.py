# -*- coding: utf-8 -*-
from dynmen.rofi import Rofi
from dynmen import new_rofi

def test_import():
    menu = Rofi()
    menu.dmenu = True
    assert menu.dmenu is True
    assert menu._trait_transformed['dmenu'] == ['-dmenu']
    assert menu._trait_transformed['font'] == []

def test_import2():
    menu = new_rofi(dmenu=False)
    assert menu.dmenu is False
    assert menu._trait_transformed['dmenu'] == []

