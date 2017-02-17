# -*- coding: utf-8 -*-
from dynmen.common import Option, Flag, TraitMenu
from dynmen.generator import AddOptions
from dynmen import ValidationError
import unittest


options = [
    Flag('version', info='print version number',
         flag='--version'),
]

@AddOptions(*options)
class Cat(TraitMenu):
    _base_command = ['cat']


class TestCat(unittest.TestCase):
    def setUp(self):
        self.cat = Cat()

    def test_repr(self):
        e = self.cat
        e.version = True
        self.assertEqual(repr(e), 'Cat(version=True)')
        e.version = False
        self.assertEqual(repr(e), 'Cat()')

    def test_validate_flag(self):
        with self.assertRaises(ValidationError):
            self.cat.version = 'asdf'

    def test_value(self):
        e = self.cat
        e.newline = True
        txt = u'müslifresser1796', u'yup', u'another'
        output = e(txt)
        self.assertEqual('\n'.join(txt), output.selected)
        
    def test_cmd(self):
        e = self.cat
        self.assertEqual(e.command, ['cat',])
        e.version = True
        self.assertEqual(e.command, ['cat', '--version'])
        del e.version
        self.assertEqual(e.command, ['cat',])
        e.version = True
        self.assertEqual(e.command, ['cat', '--version'])
        e.version = False
        self.assertEqual(e.command, ['cat',])
