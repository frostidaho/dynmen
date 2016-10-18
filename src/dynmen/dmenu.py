# -*- coding: utf-8 -*-
from dynmen.common import TraitMenu, Flag, Option

class DMenu(TraitMenu):
    case_insensitive = Flag('case_insensitive', flag='-i')
    # prompt = Option('prompt', default='', opt='-p')
    prompt = Option('prompt', default='Input: ', opt='-p')
    lines = Option('lines', default=15, opt='-l')
    # hide_scrollbar = Flag('hide_scrollbar', flag='-hide-scrollbar')

    def __init__(self, *dmenu_args, **kwargs):
        super(DMenu, self).__init__(['dmenu'])
        self.command.extend(dmenu_args)
        for k,v in kwargs.items():
            setattr(self, k, v)

