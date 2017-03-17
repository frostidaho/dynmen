import sys as _sys
class_template = """
from dynmen.common import TraitMenu, Flag, Option

class {typename}(TraitMenu):
{attributes}
    pass

"""
attr_template = """    {name} = {value}"""

def get_klass_defn(typename, *attributes):
    frmt = attr_template.format
    attrs = [frmt(typename=typename, **d) for d in attributes]
    return class_template.format(
        typename=typename,
        attributes='\n'.join(attrs),
    )

def create_class(typename, *attributes):
    namespace = dict(__name__='traitmenu_%s' % typename)
    defn = get_klass_defn(typename, *attributes)
    exec(defn, namespace)
    res = namespace[typename]
    res._source = defn

    module = _sys._getframe(1).f_globals.get('__name__', '__main__')
    if module is not None:
        res.__module__ = module
    return res

def make_attribute(name, callable_name, *args, **kwargs):
    args = [repr(x) for x in args]
    total = [callable_name, '(']
    for k,v in kwargs.items():
        txt = '{}={!r}'.format(k, v)
        args.append(txt)
    total.append(', '.join(args))
    total.append(')')
    value = ''.join(total)
    d = {
        'value': value,
        'name': name,
    }
    return d


if __name__ == '__main__':
    attrs = [
        make_attribute('dmenu', 'Flag', '-dmenu', default_value=True),
        make_attribute('font', 'Option', '-font', 'sans 24'),
    ]

    SwagBot = create_class('SwagBot', *attrs)

