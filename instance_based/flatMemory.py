from Case import Case
from Attributes import CategoricalAttr, RealAttr, Attribute
from CBRFunctions import normalize, weightedSum

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

    def __del__(self):
        pass

    def __retrieve(self,case):
        """ Retrieve the most similar case(s) """
        similarities = []
        for c in self.cases:
            similarities.append(c.similarity(case))
        types = case.types()
        sim = []
        for i in xrange(0,self.num_dim):
            sim.append(list(zip(*similarities)[i]))
            if types[i] == 'r':
                sim[i] = normalize(sim[i])
        similarities = []
        for i in xrange(0,self.num_dim):
            similarities.append(sim[i])

        similarities = zip(*similarities)

        ## Here we have the similarities of each case
        weighted_similarities = map(weightedSum, similarities)
        print 'ws'
        print weighted_similarities
        print '5 most similar'
        for v in sorted(weighted_similarities)[1:5]:
            print v

    def retrieve(self,case):
        """ Retrieve the most similar case(s) """
        return self.__retrieve(case)

    def printFlatMemory(self):
        for c in self.cases:
            c.printCase()
        print '\n Num of cases: %d' % self.num_cases

