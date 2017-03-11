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

def assert_record(rec, name, value, transformed):
    assert rec == (name, value, transformed)

def assert_future(future, selected, value):
    out = future.result(MAX_WAIT)
    assert out.selected == selected
    assert out.value == value

def test_flag(grep):
    assert_record(grep.ignore_case, 'ignore_case', False, [])
    grep.ignore_case = True
    assert_record(grep.ignore_case, 'ignore_case', True, ['-i'])
    grep.ignore_case = False
    assert_record(grep.ignore_case, 'ignore_case', False, [])

def test_option(grep):
    assert_record(grep.pattern, 'pattern', None, [])
    txt = 'some pattern'
    grep.pattern = txt
    assert_record(grep.pattern, 'pattern', txt, ['-e', txt])
    grep.pattern = None
    assert_record(grep.pattern, 'pattern', None, [])

def test_usage(grep):
    grep.menu.process_mode = 'futures'
    inp = list('abcdefghijklmnopqrstuv')
    grep.pattern = 'm'
    future = grep(inp)
    assert_future(future, 'm', None)

def test_usage_fail(grep):
    grep.menu.process_mode = 'futures'
    inp = list('abcdefghijklmnopqrstuv')
    grep.pattern = 'M'
    future = grep(inp)
    with pytest.raises(MenuError):
        future.result(MAX_WAIT)

def test_usage_update(grep):
    grep.menu.process_mode = 'futures'
    inp = list('abcdefghijklmnopqrstuv')
    grep.pattern = 'o'
    assert_future(grep(inp), 'o', None)
    grep.pattern = 'C'
    with pytest.raises(MenuError):
        grep(inp).result(MAX_WAIT)
    grep.ignore_case = True
    assert_future(grep(inp), 'c', None)
