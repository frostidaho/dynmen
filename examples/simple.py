#!/usr/bin/env python
from dynmen.rofi import Rofi

rofi = Rofi()
out_rofi = rofi(['a', 'b', 'c'])
print(out_rofi)

# TODO: Add support for non-strings?
from collections import OrderedDict
some_dict = OrderedDict((str(x), x**2) for x in range(20))

from dynmen.fzf import FZF
fzf = FZF(prompt='some prompt for fzf:')
out_fzf = fzf(some_dict)
print(out_fzf)


import textwrap
txt = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
txt = textwrap.wrap(txt, width=40)

from dynmen.dmenu import DMenu
dmenu = DMenu()
dmenu.prompt = 'some prompt for dmenu'
out_dmenu = dmenu(txt)
print(out_dmenu)
