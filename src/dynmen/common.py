# -*- coding: utf-8 -*-
import traitlets as tr
from menu import Menu as _Menu


class TraitMenu(tr.HasTraits):
    executable = tr.List(
        trait=tr.CUnicode(),
        default_value=[''],
    )

    menu = tr.Instance(klass=_Menu)

    def __init__(self, **kwargs):
        """Initialize the menu.

        All of the key-word args in kwargs are simply set
        as parameters on the instance.

        e.g., Rofi(width=50)
        which is equivalent to
              menu = Rofi()
              menu.width = 50
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.menu = _Menu(self.executable)

