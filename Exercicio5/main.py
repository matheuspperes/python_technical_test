import unittest
import io


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        
class Tree:
    def __init__(self, root=None):
        self.root = root
        self.children = {}
        
    def add_child(self, parent, child):
        if parent not in self.children:
            self.children[parent] = []
        self.children[parent].append(child)

    def add_root(self, root):
        if self.root is not None:
            raise Exception("The tree already has a root")
        self.root = root
        
    def depth_first_traversal(self, node=None, output=None):
        if node is None:
            node = self.root
        if output is None:
            output = io.StringIO()

        output = io.StringIO()
        output.write(str(node.getvalue()) + "\n")
        if node in self.children:
            for child in self.children[node]:
                output.write(self.depth_first_traversal(child))

        return output.getvalue()
            
class TestTree(unittest.TestCase):
    def setUp(self):
        # Creating nodes
        self.root = Node(1)
        self.node2 = Node(2)
        self.node3 = Node(3)
        self.node4 = Node(4)
        self.node5 = Node(5)
        
        # Creating the tree
        self.tree = Tree(self.root)
        self.tree.add_child(self.root, self.node2)
        self.tree.add_child(self.root, self.node3)
        self.tree.add_child(self.node2, self.node4)
        self.tree.add_child(self.node2, self.node5)

    def test_add_root(self):
        with self.assertRaises(Exception):
            self.tree.add_root(Node(0))
        
    def test_depth_first_traversal(self):
        expected_output = "1\n2\n4\n5\n3\n"
        output = io.StringIO()
        self.tree.depth_first_traversal(output)
        self.assertEqual(output.getvalue(), expected_output)

    def test_add_child(self):
        self.assertEqual(len(self.root.children), 2)
        self.assertEqual(self.root.children[0], self.node2)
        self.assertEqual(self.root.children[1], self.node3)
        self.assertEqual(len(self.node2.children), 2)
        self.assertEqual(self.node2.children[0], self.node4)
        self.assertEqual(self.node2.children[1], self.node5)
        
if __name__ == '__main__':
    unittest.main()