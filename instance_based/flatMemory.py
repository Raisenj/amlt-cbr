from Case import Case
from Attributes import CategoricalAttr, RealAttr, Attribute
from CBRFunctions import normalize
from operator import itemgetter

class flatMemory:
    """ A flt memory implementation """

    def __init__(self, cases):
        try:
            assert(isinstance(cases, list))
            assert(all([isinstance(case, Case) for case in cases]))
            assert(all([case.attributes.keys() == cases[0].attributes.keys()
                for case in cases]))
        except AssertionError:
            raise Exception("Invalid cases")

        self.num_cases = len(cases)
        self.num_dim = len(cases[0].attributes)
        self.cases = cases
        self.maximum = {}
        self.minimum = {}
        self.solutions = []

        for (k, v) in cases[0].attributes.items():
            if isinstance(v, RealAttr):
                self.maximum[k] = float('-inf')
                self.minimum[k] = float('inf')
            else:
                self.maximum[k] = None
                self.minimum[k] = None

        for c in cases:
            for (k, v) in c.attributes.items():
                if isinstance(v, RealAttr):
                    self.minimum[k] = min(self.minimum[k], v.askValue())
                    self.maximum[k] = max(self.maximum[k], v.askValue())
            for k in c.label.values():
                if not k.askValue() in self.solutions:
                    self.solutions.append(k.askValue())


    def __del__(self):
        pass

    def retrieve(self, case, k = 1):
        """ Retrieve the most similar case(s) """
        similarities = [c.similarity(case, self.minimum, self.maximum)
                        for c in self.cases]

        similarities = zip(range(0, self.num_cases), similarities)
        similarities.sort(key = itemgetter(1))

        return [(self.cases[index],sim) for (index,sim) in similarities[:min(self.num_cases, k)]]


    def retain(self, case):
        found = False
        for c in self.cases:
            if c.compare(case):
                found = True

        if not found:
            self.cases.append(case)

            for (k,v) in case.attributes.items():
                if isinstance(v, RealAttr):
                    self.minimum[k] = min(self.minimum[k],case.attributes[k].askValue())
                    self.maximum[k] = max(self.maximum[k], case.attributes[k].askValue())
            for k in case.label.values():
                if not k.askValue() in self.solutions:
                    self.solutions.append(k.askValue())
    
            self.num_cases +=1



    def printMemory(self):
        for c in self.cases:
            c.printCase()
        print '\n Num of cases: %d' % self.num_cases
        print '\n Max: ', self.maximum
        print '\n Min: ', self.minimum

