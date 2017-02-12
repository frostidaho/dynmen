# -*- coding: utf-8 -*-
from dynmen import Menu, MenuResult
from functools import partial
import unittest


class TestFirstItem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.head = Menu(('head', '-n1'))

    def assertMenuResultEqual(self, menu_result, selected, value=None, returncode=0):
        self.assertIsInstance(menu_result, MenuResult)
        self.assertEqual(menu_result.selected, selected)
        self.assertEqual(menu_result.value, value)
        self.assertEqual(menu_result.returncode, returncode)

    def test_ascii(self):
        res = self.head(['a', 'b', 'c'])
        self.assertMenuResultEqual(res, 'a')

    def test_unicode(self):
        res = self.head([u'ä', u'ü', u'π'])
        self.assertMenuResultEqual(res, u'ä')

    def test_notexplicit(self):
        res = self.head(['π', 'ü', 'ä'])
        self.assertMenuResultEqual(res, 'π')


    def test_dict_notexplicit(self):
        d = {
            'a': 'äää',
        }
        res = self.head(d)
        self.assertMenuResultEqual(res, 'a', 'äää')

    def test_dict_unicode_val(self):
        d = {
            'a': u'äää',
        }
        res = self.head(d)
        self.assertMenuResultEqual(res, 'a', u'äää')


