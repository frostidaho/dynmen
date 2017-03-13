# -*- coding: utf-8 -*-
from dynmen.dmenu import DMenu
from dynmen import new_dmenu
import pytest

def test_import():
    menu = DMenu()
    assert menu._trait_transformed['i'] == []
    assert menu.i is False
    menu.i = True
    assert menu.i is True
    assert menu._trait_transformed['i'] == ['-i']

def test_import2():
    menu = new_dmenu(i=True)
    assert menu.i is True
    assert menu._trait_transformed['i'] == ['-i']
