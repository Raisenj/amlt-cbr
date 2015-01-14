from Case import Case
import numpy
from numpy import median
import copy

class Node:
    """ Binary tree node """

    def __init__(self, left = None, right = None, data = None):
        self.left = left
        self.right = right
        self.data = data

class kdTree:
    """ A k-d tree implementation """

    def __init__(self, cases):
        try:
            assert(isinstance(cases, list))
            #assert(all([isinstance(case, Case) for case in cases]))
            assert(all([case.keys() == cases[0].keys() for case in cases]))
        except AssertionError:
            raise Exception("Invalid library structure to construct kd-tree")

        self.num_cases = len(cases)
        self.num_dim = len(cases[0])
        self.attribute_names = cases[0].keys()
        self.cat_attributes = [name for (name, value) in cases[0].items()
            if not isinstance(value, int)]
        #self.cat_attributes = [name for (name, value) in cases[0].items()
        #    if isinstance(value, CategoricalAtrr)]
        self.num_attributes = [name for (name, value) in cases[0].items()
            if isinstance(value, int)]

        self.root = self.__construct_tree(cases, 0, self.num_attributes)

    def __del__(self):
        pass

    def __construct_tree(self, cases, depth, attributes):
        """ Constructs a kd-tree recursively """

        n = len(cases)
        # Recursion base case
        if n == 1:
            return Node(None, None, cases)

        while len(attributes) > 0:
            # Select dimensions cyclically
            k = depth % len(attributes)
            attr = attributes[k]

            # Sort to check homogeneity & find median
            values = [case[attr] for case in cases]
            values.sort()

            # If this dimension is not homogeneous proceed
            if values[0] != values[-1]:
                threshold = median(numpy.array(values))

                # Partition the data according to the threshold
                left_cases = [case for case in cases if case[attr] <= threshold]
                right_cases = [case for case in cases if case[attr] > threshold]
                return Node(
                        self.__construct_tree(left_cases, depth + 1, attributes),
                        self.__construct_tree(right_cases, depth + 1, attributes),
                        (attr, threshold))
            # If it is, remove this attribute from the list
            else:
                attributes = copy.copy(attributes)
                attributes.remove(attr)

        # All the dimensions in this region are constant
        return Node(None, None, cases)

    def __print_leafs(self, node):
        """ Debug method to inspect the tree """

        # If its a leaf node, print cases
        if node.left == None and node.right == None:
            print "Leaf: "
            for case in node.data:
                print case
            return

        # Otherwise, go left and then right
        self.__print_leafs(node.left, index)
        self.__print_leafs(node.right, index)

    def __retrieve(self, case, node):
        """ Retrieve the most similar cases(s) """

        # We hit a leaf node
        if node.left == None and node.right == None:
            return node.data

        # Otherwise, traverse the tree
        attribute_name = node.data[0]
        threshold = node.data[1]
        if case[attribute_name] <= threshold:
            return self.__retrieve(case, node.left)
        else:
            return self.__retrieve(case, node.right)

    def retrieve(self, case):
        """ Retrieve the most similar cases(s) """
        return self.__retrieve(case, self.root)

if __name__ == "__main__":
    import random
    cases = []
    for i in xrange(100):
        cases.append(dict(zip(range(1, 10),
            [random.randint(0,100) for r in xrange(10)])))

    tree = kdTree(cases)
    tree._kdTree__print_leafs(tree.root)
