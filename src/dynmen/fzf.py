# -*- coding: utf-8 -*-
from dynmen.common import TraitMenu, Flag, Option


class FZF(TraitMenu):
    _base_command = ['fzf']
    case_insensitive = Flag(
        'case_insensitive',
        flag='-i',
        info='Case insensitive matching',
    )
    prompt = Option(
        'prompt',
        default='Input: ',
        flag='--prompt',
        info='Display text to the left of the input',
    )
