import logging
logr = logging.getLogger(__name__)
logr.addHandler(logging.NullHandler())

def format_code(source):
    import yapf
    from yapf.yapflib.yapf_api import FormatCode
    SetGlobalStyle = yapf.style.SetGlobalStyle
    cfg = yapf.style.CreatePEP8Style()
    cfg['ALLOW_MULTILINE_DICTIONARY_KEYS'] = True
    cfg['COLUMN_LIMIT'] = 90
    cfg['DEDENT_CLOSING_BRACKETS'] = True
    SetGlobalStyle(cfg)
    source, changed = FormatCode(source)
    return source

class Code(object):
    _template = ''
    level = 0
    indent = '    '
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        indent = self.indent * self.level
        return indent + self._template.format(**self.__dict__)

    def __repr__(self):
        clsname = self.__class__.__name__
        total = [clsname, '(**', repr(self.__dict__), ')']
        return ''.join(total)

class Assignment(Code):
    _template = '{name} = {value!r}'

    def __init__(self, name, value, **kwargs):
        super(Assignment, self).__init__(name=name, value=value, **kwargs)

class Callable(Code):
    _template = '{name} = {call_name}({total_args})'
    def __init__(self, name, call_name, *pargs, **kwargs):
        self.name = name
        self.call_name = call_name
        total_args = [repr(x) for x in pargs]
        for k,v in kwargs.items():
            val = '{}={!r}'.format(k, v)
            total_args.append(val)
        self.total_args = ', '.join(total_args)

class Flag(Callable):
    call_name = 'Flag'
    def __init__(self, flag, *pargs, **kwargs):
        name = self.str_to_ident(flag)
        super(Flag, self).__init__(name, self.call_name, flag, *pargs,
                                   **kwargs)

    @staticmethod
    def str_to_ident(txt):
        import re
        clean = lambda varStr: re.sub('\W|^(?=\d)','_', varStr)
        txt =  txt.lstrip('-')
        return clean(txt)

class Option(Flag):
    call_name = 'Option'

_menu_template = """
from dynmen.common import TraitMenu, Flag, Option
class {typename}(TraitMenu):
{attributes}
"""
class MenuType(Code):
    _template = _menu_template
    def __init__(self, typename, *attributes):
        if attributes:
            attrs = []
            for attr in attributes:
                attr.level += 1
                attrs.append(str(attr))
        else:
            indent = (self.level + 1) * self.indent
            attrs = [indent + 'pass']
        super(MenuType, self).__init__(
            typename=typename,
            attributes='\n'.join(attrs),
        )


    def __str__(self):
        txt = super(MenuType, self).__str__()
        try:
            return format_code(txt)
        except ImportError:
            logr.warning("Couldn't import 'yapf'; generated code won't be formatted")
            return txt

    def create_class(self):
        """Although we're primarily interested in the source of the class

        we create it here, just to ensure there aren't any errors
        """
        import sys
        typename = self.typename
        supercls = type(self).__name__
        namespace = dict(__name__='{}_{}'.format(supercls, typename))
        defn = str(self)
        exec(defn, namespace)
        res = namespace[typename]
        res._source = defn
        module = sys._getframe(1).f_globals.get('__name__', '__main__')
        if module is not None:
            res.__module__ = module
        return res

if __name__ == '__main__':
     x = Assignment(name='x', value=37)
     y = Assignment('y', 'asdf test 1 2 3')
     dmenu = Flag('-dmenu', default_value=True)
     display = Option('-display', default_value=-1, info_text='some info')
     someclass_src = MenuType('SomeClass', x, y, dmenu, display)
     print(someclass_src)                     # stop here if you just need the module source
     SomeClass = someclass_src.create_class() # if you actually want to generate the class
        
