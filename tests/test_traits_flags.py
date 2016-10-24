# -*- coding: utf-8 -*-
from dynmen import common, ValidationError
from operator import attrgetter
import unittest

class TestFlag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class TFlag(object):
            dflt_t = common.Flag('dflt_t', default=True, flag='-dt', info='default true')
            dflt_f = common.Flag('dflt_f', default=False, flag='-df', info='default false')
        cls.TFlag = TFlag

    def setUp(self):
        self.tflag = self.TFlag()

    def assertRecordKeysEql(self, rec, **kwargs):
        for k,v in kwargs.items():
            self.assertEqual(getattr(rec, k), v)

    def assertRecordEqualDeflt(self, name):
        rec_inst = getattr(self.tflag, name)
        rec_cls = getattr(self.TFlag, name)
        self.assertEqual(rec_inst, rec_cls)

    def test_dflt_true(self):
        self.assertRecordKeysEql(
            self.tflag.dflt_t,
            name='dflt_t',
            type='Flag',
            info='default true',
            value=True,
        )
        self.tflag.dflt_t = False
        self.assertRecordKeysEql(
            self.tflag.dflt_t,
            name='dflt_t',
            type='Flag',
            info='default true',
            value=False,
        )

    def test_dflt_true_trans(self):
        self.assertRecordKeysEql(
            self.tflag.dflt_t,
            value=True,
            transformed=['-dt'],
        )
        self.tflag.dflt_t = False
        self.assertRecordKeysEql(
            self.tflag.dflt_t,
            value=False,
            transformed=[],
        )

    def test_dflt_false_trans(self):
        self.assertRecordKeysEql(
            self.tflag.dflt_f,
            value=False,
            transformed=[],
        )
        self.tflag.dflt_f = True
        self.assertRecordKeysEql(
            self.tflag.dflt_f,
            value=True,
            transformed=['-df'],
        )

    def test_validation(self):
        with self.assertRaises(ValidationError):
            self.tflag.dflt_t = 42

# def assertRecordEqual(self, rec):
#     name = rec.name
#     for dfltrec in self.tflag.default_settings:
#         if name == dfltrec.name:
#             break
#     else:
#         raise Exception("Name didn't match any default record! {}".format(name))
#     self.assertEqual(rec, dfltrec)
