# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from dynmen.common import TraitMenu, Option, Flag
from dynmen.menu import MenuError


class Grep(TraitMenu):
    _base_command = ['grep']
    ignore_case = Flag('-i', help='ignore case')
    pattern = Option('-e', help='regex pattern')


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


def test_update_base():
    grep = Grep(ignore_case=True)
    grep._needs_update = False
    grep.base_command = ['cat']
    assert grep._needs_update


def test_process_mode(grep):
    pm = grep.process_mode
    assert pm == grep._menu.process_mode
    grep.process_mode = 'async'
    assert grep.process_mode == 'async'
    assert grep._menu.process_mode == 'async'


def compare_alias(obj, name0, name1):
    assert getattr(obj, name0) == getattr(obj, name1)
    assert obj._trait_transformed[name0] == obj._trait_transformed[name1]


def test_alias():
    class Grep2(Grep):
        _aliases = (
            ('ignore_case', 'case_insensitive'),
        )
    grep = Grep2()
    compare_alias(grep, 'ignore_case', 'case_insensitive')
    grep.ignore_case = True
    assert grep._trait_transformed['ignore_case'] == ['-i']
    compare_alias(grep, 'ignore_case', 'case_insensitive')
    grep.case_insensitive = False
    compare_alias(grep, 'ignore_case', 'case_insensitive')


def test_help_msg(grep):
    cls = grep.__class__
    assert cls.ignore_case.help == 'ignore case'
    assert cls.pattern.help == 'regex pattern'
