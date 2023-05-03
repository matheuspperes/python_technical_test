import re
import unittest
from bigtree import dict_to_tree, print_tree

class TestBigTree(unittest.TestCase):

    def setUp(self):
        self.path_dict = {
            "a": {"age": 90},
            "a/b": {"age": 65},
            "a/c": {"age": 60},
            "a/b/d": {"age": 40},
            "a/b/e": {"age": 35},
        }
        self.root = dict_to_tree(self.path_dict)

    def test_dict_to_tree(self):
        self.assertEqual(self.root.name, 'a')
        self.assertEqual(self.root.children[0].name, 'b')
        self.assertEqual(self.root.children[1].name, 'c')
        self.assertEqual(self.root.children[0].children[0].name, 'd')
        self.assertEqual(self.root.children[0].children[1].name, 'e')
        self.assertEqual(self.root.children[0].children[0].attr['age'], 40)
        self.assertEqual(self.root.children[0].children[1].attr['age'], 35)

    def test_print_tree(self):
        # Redirect print output to a buffer
        import io
        import sys
        buffer = io.StringIO()
        sys.stdout = buffer

        # Print the tree with age attributes
        print_tree(self.root, attr_list=["age"])

        # Get the printed output
        output = buffer.getvalue().strip()
        sys.stdout = sys.__stdout__

        # Test that each node is printed with the expected format
        expected_formats = {
            'a': r'a \[age=90\]',
            'b': r'b \[age=65\]',
            'c': r'c \[age=60\]',
            'd': r'd \[age=40\]',
            'e': r'e \[age=35\]',
        }
        for node, expected_format in expected_formats.items():
            pattern = re.escape(expected_format)
            self.assertRegex(output, f'^{node} {pattern}$')

if __name__ == '__main__':
    unittest.main()