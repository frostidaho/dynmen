from dynmen.common import (
    TraitMenu,
    Flag,
    Option,
)
from itertools import islice
from types import GeneratorType as _GeneratorType

class SimpleRofi(TraitMenu):
    _base_command = ['rofi', '-dmenu']

    entry_sep = Option('-sep', default_value='\0')
    case_insensitive = Flag('-i', default_value=False)
    prompt = Option('-p')
    element_height = Option('-eh')
    lines = Option('-lines')

    font = Option('-font')

    display = Option('-display')
    location = Option('-location')
    padding = Option('-padding')
    fullscreen = Flag('-fullscreen')


    def __call__(self, entries=(), entry_sep=None, **kw):
        if isinstance(entries, _GeneratorType):
            entries = list(entries)
        self.element_height = self._get_element_height(entries)

        super(SimpleRofi, self).__call__(
            entries,
            entry_sep=entry_sep,
            **kw,
        )

    @staticmethod
    def _get_element_height(entries, check_n=None):
        if check_n is not None:
            entries = islice(entries, check_n)
        else:
            entries = iter(entries)
        return max((x.count('\n') for x in entries)) + 1


