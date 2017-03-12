# -*- coding: utf-8 -*-
from dynmen.rofi import Rofi
from dynmen import new_rofi

def test_import():
    menu = Rofi()
    menu.dmenu = True
    assert menu.dmenu.value is True
    assert menu.font.transformed == []

def test_import2():
    menu = new_rofi(dmenu=False)
    assert menu.dmenu.value is False

