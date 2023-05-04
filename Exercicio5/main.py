import unittest


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
    
    def add_child(self, child_node):
        self.children.append(child_node)
        
class Tree:
    def __init__(self, root=None):
        self.root = root
        
    def add_node(self, parent_node, child_node):    # function to add node as child
        parent_node.add_child(child_node)         
        
    def traverse_pre_order(self, node, output):     
        output.append(node.value)                   
        for child in node.children:
            self.traverse_pre_order(child, output)  # Recursively call the function method with each child of current node after appending node
    
class TestTree(unittest.TestCase):
    def setUp(self):
        # create the tree
        self.root = Node(1)                     # creates node with value 1 
        self.child1 = Node(2)                   # creates node with value 2 
        self.child2 = Node(3)                   # creates node with value 3 
        self.grandchild1 = Node(4)              # creates node with value 4 
        self.grandchild2 = Node(5)              # creates node with value 5 
        
        self.child1.add_child(self.grandchild1) # add node4 as child of node2
        self.child2.add_child(self.grandchild2) # add node5 as child of node3
        
        self.root.add_child(self.child1)        # add node2 as child of root
        self.root.add_child(self.child2)        # add node3 as child of root
        self.tree = Tree(self.root)             # create tree
        
        # 1 -> 2 -> 4
        #   -> 3 -> 5

    def test_add_node(self):
        # test adding a node6 to the tree
        new_node = Node(6)                                      # creates node with value 6
        self.tree.add_node(self.grandchild1, new_node)          # add node6 as child of node4
        self.assertEqual(self.grandchild1.children[0].value, 6) # assert node6 just added
        
        # 1 -> 2 -> 4 -> 6
        #   -> 3 -> 5

    def test_traverse_pre_order(self):
        # test pre-order traversal
        expected_output = [1, 2, 4, 3, 5]               # expected value after traversal order function following node sequence
        output = []
        self.tree.traverse_pre_order(self.root, output)
        self.assertEqual(output, expected_output)
        # print(output)

if __name__ == '__main__':
    unittest.main()