from Case import Case
from Attributes import CategoricalAttr, RealAttr, Attribute
from CBRFunctions import normalize

class flatMemory:
    """ A flt memory implementation """

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
        self.cases = cases
        self.maximum = {}
        self.minimum = {}
       
        for (k,v) in cases[0].attributes.items():
            if isinstance(v,RealAttr):
                self.maximum[k] = float('-inf')
                self.minimum[k] = float('inf')

        for c in cases:
            for (k,v) in c.attributes.items():
                if isinstance(v,RealAttr):
                    self.minimum[k] = min(self.minimum[k],v.askValue())
                    self.maximum[k] = max(self.maximum[k],v.askValue())


    def __del__(self):
        pass

    def __retrieve(self,case):
        """ Retrieve the most similar case(s) """
        similarities = []
        for c in self.cases:
            similarities.append(c.similarity(case,self.minimum,self.maximum))
        return similarities
                    
    def retrieve(self,case):
        """ Retrieve the most similar case(s) """
        return self.__retrieve(case)

    def printFlatMemory(self):
        for c in self.cases:
            c.printCase()
        print '\n Num of cases: %d' % self.num_cases
    def askCae(self, index):
        return self.cases[index]

