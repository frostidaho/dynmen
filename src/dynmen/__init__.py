# -*- coding: utf-8 -*-
"""
dynmen - A simple python interface to dynamic menus like dmenu or rofi

import dynmen
menu = dynmen.Menu(['dmenu', '-fn', 'Sans-30'])
output = menu({'a': 1, 'b': 2, 'c': 3})

You can make the menu non-blocking by setting:
   menu.process_mode = 'futures'

Please see the repository for more examples:
    https://github.com/frostidaho/dynmen
"""
from .menu import Menu, MenuError
del menu


def new_dmenu(**kwargs):
    from .dmenu import DMenu
    return DMenu(**kwargs)


def new_rofi(**kwargs):
    from .rofi import Rofi
    return Rofi(**kwargs)
