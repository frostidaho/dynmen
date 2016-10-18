# -*- coding: utf-8 -*-
from dynmen.common import TraitMenu, Flag, Option

class FZF(TraitMenu):
    case_insensitive = Flag('case_insensitive', flag='-i')
    prompt = Option('prompt', default='Input: ', opt='--prompt')

    def __init__(self, *fzf_args, **kwargs):
        super(FZF, self).__init__(['fzf'])
        self.command.extend(fzf_args)
        for k,v in kwargs.items():
            setattr(self, k, v)

