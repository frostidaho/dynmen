# -*- coding: utf-8 -*-
from .menu import Menu, MenuError
del menu

def new_dmenu(**kwargs):
    from .dmenu import DMenu
    return DMenu(**kwargs)

def new_rofi(**kwargs):
    from .rofi import Rofi
    return Rofi(**kwargs)

