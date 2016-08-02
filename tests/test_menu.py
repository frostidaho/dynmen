from dynmen import Menu, MenuResult
from functools import partial
import unittest


class TestCat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = Menu(('cat',))

    def test_restype(self):
        res = self.cat('abcd')
        self.assertIsInstance(res, MenuResult)

    def test_result(self):
        data = 'abcd'
        res = self.cat(data)
        self.assertEqual(res.selected, '\n'.join(data))


class TestGrep(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = {
            'groupname': 'Root',
            'notes': 'Maaskantje',
            'password': 'SoEinFeuerballJunge',
            'title': 'npr.org',
            'url': 'https://www.youtube.com/watch?v=yrtUKe5Q82w',
            'username': 'müslifresser1796',
        }

    def setUp(self):
        self.grep = Menu(['grep',])

    def test_dict(self):
        grep_str = 'title'
        self.grep.command.append(grep_str)
        res = self.grep(self.data)
        self.assertEqual(res.selected, grep_str)
        self.assertEqual(res.value, self.data[grep_str])

    def test_list(self):
        grep_str = 'username'
        self.grep.command.append(grep_str)
        res = self.grep(list(self.data))
        self.assertEqual(res.selected, grep_str)
        self.assertEqual(res.value, None)

    def test_generator(self):
        grep_str = 'url'
        self.grep.command.append(grep_str)
        res = self.grep(x for x in self.data.keys())
        self.assertEqual(res.selected, grep_str)
        self.assertEqual(res.value, None)


class TestSort(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = ('c', 'a', 'b')
        cls.cat = Menu(['cat',])

    def setUp(self):
        self.grep = Menu(['grep',])

    def test_sort_regular(self):
        res = self.cat.sort(self.data)
        self.assertEqual(res.selected, '\n'.join(sorted(self.data)))
        self.assertIs(res.value, None)

    def test_sort_reverse(self):
        res = self.cat.sort(self.data, reverse=True)
        self.assertEqual(
            res.selected,
            '\n'.join(sorted(self.data, reverse=True)),
        )
        self.assertIs(res.value, None)

    def test_sort_dict_val(self):
        d = dict((x[1], x[0]) for x in enumerate(self.data))
        grep_str = self.data[0]
        self.grep.command.append(grep_str)
        res = self.grep.sort(d)
        self.assertEqual(res.selected, grep_str)
        self.assertIs(res.value, 0)

