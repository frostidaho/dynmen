# -*- coding: utf-8 -*-
from dynmen import common, ValidationError
from dynmen.common import Option
from operator import attrgetter
import unittest

class TestOpts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class TOpt(object):
            prompt = Option(
                'prompt',
                default='Input: ',
                flag='-p',
                info='Display text to the left of the input',
            )
            lines = Option(
                'lines',
                default=15,
                flag='-l',
                info='Number of lines to display. (Does not work with fullscreen)',
                dtype=int,
            )
        cls.TOpt = TOpt

    def setUp(self):
        self.to = self.TOpt()

    def assertRecordKeysEql(self, rec, **kwargs):
        name = rec.name
        d_rec = getattr(self.TOpt, name).default_record._asdict()
        d_rec.update(kwargs)
        for key in rec._fields:
            val = getattr(rec, key)
            self.assertEqual(val, d_rec[key])

    def test_lines(self):
        rec = self.to.lines
        self.assertRecordKeysEql(rec)
        self.to.lines = 37
        self.assertRecordKeysEql(self.to.lines, value=37, transformed=['-l', '37'])
        self.to.lines = '42'
        self.assertRecordKeysEql(self.to.lines, value=42, transformed=['-l', '42'])
        x = 30.1
        self.to.lines = 30.1
        self.assertRecordKeysEql(self.to.lines, value=int(x), transformed=['-l', '30'])

    def test_lines_fail(self):
        with self.assertRaises(ValidationError):
            self.to.lines = 'asdfadfasdf'

    # def test_lines_fail(self):
    #     self.to.lines = '37'
    #     rec = self.to.lines
    #     self.assertRecordKeysEql(rec)
    #     self.to.lines = 37
    #     self.assertRecordKeysEql(self.to.lines, value=37, transformed=['-l', '37'])
            


# def assertRecordEqual(self, rec):
#     name = rec.name
#     for dfltrec in self.tflag.default_settings:
#         if name == dfltrec.name:
#             break
#     else:
#         raise Exception("Name didn't match any default record! {}".format(name))
#     self.assertEqual(rec, dfltrec)
