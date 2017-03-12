# -*- coding: utf-8 -*-
from dynmen.dmenu import DMenu
from dynmen import new_dmenu

def test_import():
    menu = DMenu()
    menu.i = True
    assert menu.i.value is True

def test_import2():
    menu = new_dmenu(i=True)
    assert menu.i.value is True

