from Case import Case
from Attributes import CategoricalAttr, RealAttr, Attribute
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
            assert(all([isinstance(case, Case) for case in cases]))
            assert(all([case.attributes.keys() == cases[0].attributes.keys()
                for case in cases]))
        except AssertionError:
            raise Exception("Invalid library structure to construct kd-tree")

        self.num_cases = len(cases)
        self.num_dim = len(cases[0].attributes)
        #self.attribute_names = cases[0].attribute_names.keys()
        self.cat_attributes = [name for (name, value) in cases[0].attributes.items()
            if isinstance(value, CategoricalAttr)]
        self.num_attributes = [name for (name, value) in cases[0].attributes.items()
            if not isinstance(value, RealAttr)]

        self.root = self.__construct_tree(cases, 0)

    def __del__(self):
        pass

    def __construct_tree(self, cases, depth):
        """ Constructs a kd-tree recursively """

        n = len(cases)
        # Recursion base case
        if n == 1:
            return Node(None, None, cases)

        max_spread = float("-inf")
        best_attr = None
        best_threshold = None
        for attr in self.num_attributes:
            # Get and sort values
            values = numpy.array([case.attributes[attr].askValue()
                for case in cases])
            values.sort()

            # Compute statistic
            threshold = median(values)
            IQR1 = median(values[0:n//2])
            IQR3 = median(values[n//2:n])

            spread = IQR3 - IQR1
            if spread > max_spread:
                max_spread = spread
                best_threshold = threshold
                best_attr = attr

        if best_attr is not None:
            # Partition the data according to the threshold
            left_cases = [case for case in cases
                    if case.attributes[attr].askValue() < best_threshold]
            right_cases = [case for case in cases
                    if case.attributes[attr].askValue() >= best_threshold]
            return Node(
                    self.__construct_tree(left_cases, depth + 1),
                    self.__construct_tree(right_cases, depth + 1),
                    (attr, threshold))
        # All the dimensions in this region are constant
        else:
            return Node(None, None, cases)

    def __print_leafs(self, node):
        """ Debug method to inspect the tree """

        # If its a leaf node, print cases
        if node.left == None and node.right == None:
            print "Leaf: "
            for case in node.data:
                case.printCase()
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
    print 'cases'
    for c in cases:
        print c
    tree = kdTree(cases)
    tree._kdTree__print_leafs(tree.root)
