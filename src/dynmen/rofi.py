# -*- coding: utf-8 -*-
from os import path as _path
from dynmen.common import TraitMenu as _TraitMenu
from dynmen.generator import (AddOptions as _AddOptions,
                              load_options as _load_options,)


_dirname = _path.dirname(_path.abspath(__file__))
_path = _path.join(_dirname, 'data/rofi_opts.json')

@_AddOptions(*_load_options(_path))
class Rofi(_TraitMenu):
    _base_command = ['rofi']

