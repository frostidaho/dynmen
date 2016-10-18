# -*- coding: utf-8 -*-
from dynmen import common
import unittest

class TestFlag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class TFlag(object):
            dflt_t = common.Flag('dflt_t', default=True, flag='-dt')
            dflt_f = common.Flag('dflt_f', default=False, flag='-df')
        cls.TFlag = TFlag

    def setUp(self):
        self.tflag = self.TFlag()

    def test_dflt_true(self):
        self.assertEqual(self.tflag.dflt_t, '-dt')
        self.tflag.dflt_t = False
        self.assertFalse('')

    def test_dflt_false(self):
        self.assertEqual(self.tflag.dflt_f, '')
        self.tflag.dflt_f = True
        self.assertEqual(self.tflag.dflt_f, '-df')

    def test_validation(self):
        with self.assertRaises(TypeError):
            self.tflag.dflt_f = 37
        with self.assertRaises(TypeError):
            self.tflag.dflt_t = 'asdfasdf'

