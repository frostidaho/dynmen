# -*- coding: utf-8 -*-
from dynmen.common import TraitMenu, Flag, Option

class DMenu(TraitMenu):
    case_insensitive = Flag('case_insensitive', flag='-i', info='Case insensitive matching')
    prompt = Option(
        'prompt',
        default='Input: ',
        flag='-p',
        info='Display text to the left of the input',
    )
    lines = Option(
        'lines',
        default=15,
        flag='-l',
        info='Number of lines to display. (Does not work with fullscreen)',
        type=int,
    )

    def __init__(self, *dmenu_args, **kwargs):
        super(DMenu, self).__init__(['dmenu'])
        self.command.extend(dmenu_args)
        for k,v in kwargs.items():
            setattr(self, k, v)

