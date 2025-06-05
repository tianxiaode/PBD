import unittest
from pbd_core import DictHelper

class TestDictHelper(unittest.TestCase):

    def test_flatten_happy_path(self):
        input_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        expected_output = {'a': 1, 'b.c': 2, 'b.d.e': 3}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_empty_dict(self):
        input_dict = {}
        expected_output = {}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_single_level_dict(self):
        input_dict = {'x': 10, 'y': 20, 'z': 30}
        expected_output = {'x': 10, 'y': 20, 'z': 30}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_nested_empty_dict(self):
        input_dict = {'a': {}, 'b': {'c': {}}}
        expected_output = {'a': {}, 'b.c': {}}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_with_different_separator(self):
        input_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        expected_output = {'a': 1, 'b_c': 2, 'b_d_e': 3}
        self.assertEqual(DictHelper.flatten(input_dict, sep='_'), expected_output)

    def test_flatten_with_parent_key(self):
        input_dict = {'a': 1, 'b': {'c': 2}}
        expected_output = {'root.a': 1, 'root.b.c': 2}
        self.assertEqual(DictHelper.flatten(input_dict, parent_key='root'), expected_output)

    def test_flatten_with_mixed_data_types(self):
        input_dict = {'a': 1, 'b': {'c': [2, 3], 'd': {'e': 'f'}}}
        expected_output = {'a': 1, 'b.c': [2, 3], 'b.d.e': 'f'}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

    def test_flatten_with_non_dict_value(self):
        input_dict = {'a': 1, 'b': 2}
        expected_output = {'a': 1, 'b': 2}
        self.assertEqual(DictHelper.flatten(input_dict), expected_output)

if __name__ == '__main__':
    unittest.main()