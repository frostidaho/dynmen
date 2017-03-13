import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from dynmen.common import TraitMenu, Option, Flag
from dynmen.menu import MenuError

class Grep(TraitMenu):
    _base_command = ['grep']
    ignore_case = Flag('-i')
    pattern = Option('-e')

import pytest
MAX_WAIT = 3.0
@pytest.fixture(scope='function')
def grep():
    return Grep()

def assert_record(obj, name, value, transformed):
    assert getattr(obj, name) == value
    assert obj._trait_transformed[name] == transformed

def assert_future(future, selected, value):
    out = future.result(MAX_WAIT)
    assert out.selected == selected
    assert out.value == value

def test_flag(grep):
    assert_record(grep, 'ignore_case', False, [])
    grep.ignore_case = True
    assert_record(grep, 'ignore_case', True, ['-i'])
    grep.ignore_case = False
    assert_record(grep, 'ignore_case', False, [])

def test_option(grep):
    assert_record(grep, 'pattern', None, [])
    txt = 'some pattern'
    grep.pattern = txt
    assert_record(grep, 'pattern', txt, ['-e', txt])
    grep.pattern = None
    assert_record(grep, 'pattern', None, [])

def test_usage(grep):
    grep._menu.process_mode = 'futures'
    inp = list('abcdefghijklmnopqrstuv')
    grep.pattern = 'm'
    future = grep(inp)
    assert_future(future, 'm', None)

# def test_usage_fail(grep):
#     grep._menu.process_mode = 'futures'
#     inp = list('abcdefghijklmnopqrstuv')
#     grep.pattern = 'M'
#     future = grep(inp)
#     with pytest.raises(MenuError):
#         future.result(MAX_WAIT)

# def test_usage_update(grep):
#     grep._menu.process_mode = 'futures'
#     inp = list('abcdefghijklmnopqrstuv')
#     grep.pattern = 'o'
#     assert_future(grep(inp), 'o', None)
#     grep.pattern = 'C'
#     with pytest.raises(MenuError):
#         grep(inp).result(MAX_WAIT)
#     grep.ignore_case = True
#     assert_future(grep(inp), 'c', None)

# def test_trait_menu_kwargs():
#     grep = Grep(ignore_case=True)
#     assert_record(grep.ignore_case, 'ignore_case', True, ['-i'])

# def test_update_base():
#     grep = Grep(ignore_case=True)
#     grep._needs_update = False
#     grep.base_command = ['cat']
#     assert grep._needs_update == True

# def test_process_mode(grep):
#     pm = grep.process_mode
#     assert pm == grep._menu.process_mode
#     grep.process_mode = 'async'
#     assert grep.process_mode == 'async'
#     assert grep._menu.process_mode == 'async'


# def compare_alias(obj1, obj2):
#     assert obj1 == obj2
#     # assert obj1.name != obj2.name
#     # assert obj1.value == obj2.value
#     # assert obj1.transformed == obj2.transformed

# def test_alias():
#     class Grep2(Grep):
#         _aliases = (
#             ('ignore_case', 'case_insensitive'),
#         )
#     grep = Grep2()
#     compare_alias(grep.ignore_case, grep.case_insensitive)
#     grep.ignore_case = True
#     compare_alias(grep.ignore_case, grep.case_insensitive)
#     grep.case_insensitive = False
#     compare_alias(grep.ignore_case, grep.case_insensitive)

# def test_alias_menu_command():
#     class Grep2(Grep):
#         _aliases = (
#             ('ignore_case', 'case_insensitive'),
#         )
#     grep = Grep2()
#     grep.case_insensitive = True
#     compare_alias(grep.ignore_case, grep.case_insensitive)
#     assert grep.case_insensitive.transformed == ['-i']
#     assert grep.ignore_case.transformed == ['-i']
#     grep._menu_update()
#     assert grep._menu.command.count('-i') == 1

