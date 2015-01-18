from Attributes import RealAttr, CategoricalAttr, Attribute
import numpy

class Case():

    weights = None

    def __init__(self, attributes, label=None):
        self.attributes = attributes
        self.label = label
        self.utility = 0
        self.evaluation = True

    def __del__(self):
        pass

    def printCase(self):
        print '\n'
        print '====== CASE ======'
        print '-- Attributes'
        for k in self.attributes.keys():
            print k, ': ', self.attributes[k].askValue()
        print '-- Label'
        if self.label:
            for k in self.label.keys():
                print k, ': ',  self.label[k].askValue()
        else:
            print 'no label'
        print '=================='

    def types(self):
        types = []
        for k in self.attributes.keys():
            if isinstance(self.attributes[k],RealAttr):
                types.append('r')
            elif isinstance(self.attributes[k],CategoricalAttr):
                types.append('c')
        return types

    def attrNames(self):
        return self.attributes.keys()
        return names

    def labelName(self):
        return self.label.keys()[0]

    def labelValue(self):
        return self.label[self.label.keys()[0]].askValue()

    def similarity(self, case, minimums, maximums):
        sim = [v.similarity(case.attributes[k], minimums[k], maximums[k])
                for (k, v) in self.attributes.items()]
        if self.weights == None:
            return sum(sim)
        else:
            return sum(numpy.array(sim) * numpy.array(self.weights.values())) / sum(self.weights.values())
