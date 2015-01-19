from Case import Case
from Attributes import CategoricalAttr, RealAttr, Attribute
import numpy
from numpy import median
import copy
from operator import itemgetter

class Node:
    """ Binary tree node """

    def __init__(self, left = None, right = None,
                data = None, num_instances = 0):
        self.left = left
        self.right = right
        self.data = data
        self.num_instances = num_instances

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
        self.cat_attributes = [name for (name, value) in cases[0].attributes.items()
            if isinstance(value, CategoricalAttr)]
        self.num_attributes = [name for (name, value) in cases[0].attributes.items()
            if isinstance(value, RealAttr)]

        self.minimums = {}
        self.maximums = {}
        for attr in self.num_attributes:
            values = [case.attributes[attr].askValue() for case in cases]
            self.minimums[attr] = min(values)
            self.maximums[attr] = max(values)

        for attr in self.cat_attributes:
            self.minimums[attr] = None
            self.maximums[attr] = None

        self.root = self.__construct_tree(cases, 0)

    def __del__(self):
        pass

    def __construct_tree(self, cases, depth):
        """ Constructs a kd-tree recursively """

        n = len(cases)
        # Recursion base case
        if n == 1:
            return Node(None, None, cases, n)

        max_spread = 0
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

            # Normalized inter-quartile spread
            spread = (IQR3 - IQR1)/(self.maximums[attr] - self.minimums[attr])
            if spread > max_spread:
                max_spread = spread
                best_threshold = threshold
                best_attr = attr

        if best_attr is not None:
            # Partition the data according to the threshold
            left_cases = [case for case in cases
                    if case.attributes[best_attr].askValue() <= best_threshold]
            right_cases = [case for case in cases
                    if case.attributes[best_attr].askValue() > best_threshold]

            if len(left_cases) == 0 or len(right_cases) == 0:
                left_cases = [case for case in cases
                    if case.attributes[best_attr].askValue() < best_threshold]
                right_cases = [case for case in cases
                    if case.attributes[best_attr].askValue() >= best_threshold]

            return Node(
                    self.__construct_tree(left_cases, depth + 1),
                    self.__construct_tree(right_cases, depth + 1),
                    (attr, threshold), n)
        # All the dimensions in this region are constant
        else:
            return Node(None, None, cases, n)

    def printMemory(self):
        """ Debug method to inspect the tree """
        self.__printMemory(self.root)

    def __printMemory(self, node):
        """ Debug method to inspect the tree """

        # If its a leaf node, print cases
        if node.left == None and node.right == None:
            print "Leaf: "
            for case in node.data:
                case.printCase()
            return

        # Otherwise, go left and then right
        self.__printMemory(node.left, index)
        self.__printMemory(node.right, index)

    def __retrieve_all(self, node):
        """ Retrieve all the instance(s) below node """

        if node.left == None and node.right == None:
            return node.data

        return self.__retrieve_all(node.left) + self.__retrieve_all(node.right)

    def __retrieve(self, case, node, k):
        """ Retrieve the most similar cases(s) """

        # We hit a leaf node
        if node.left == None and node.right == None:
            return node.data

        # Otherwise, traverse the tree
        attribute_name = node.data[0]
        threshold = node.data[1]
        if case.attributes[attribute_name].askValue() <= threshold:
            left = node.left
            if left.num_instances < k:
                return (self.__retrieve_all(node), node)
            return self.__retrieve(case, left, k)
        else:
            right = node.right
            if right.num_instances < k:
                return (self.__retrieve_all(node), node)
            return self.__retrieve(case, right, k)

    def retrieve(self, case, k = 1):
        """ Retrieve the most similar cases(s) """

        (retrieved_cases, _) = self.__retrieve(case, self.root, k)
        n = len(retrieved_cases)

        similarities = [c.similarity(case, self.minimums, self.maximums)
                        for c in retrieved_cases]
        similarities = zip(range(0, n), similarities)
        similarities.sort(key = itemgetter(1))

        return [(retrieved_cases[index], similarity)
                for (index, similarity) in similarities[:min(n, k)]]

    def retain(self, case):
        """ Retain the given case """

        (cases, node) = self.__retrieve(case, self.root, 1)
        cases.append(case)

        new_node = self.__construct_tree(cases)
        node.data = new_node.data
        node.num_instances = new_node.num_instances
        node.right = new_node.right
        node.left = new_node.left

