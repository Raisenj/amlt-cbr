from Attributes import RealAttr, CategoricalAttr, Attribute

class Case():

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
        names = []
        for name in self.attributes.keys():
            names.append(name)
        #names.append(self.label.keys()[0])
        return names

    def labelName(self):
        return self.label.keys()[0]

    def labelValue(self):
        return self.label[self.label.keys()[0]].askValue()


    def similarity(self, case, minimum, maximum):
        sim = {}
        for (k,v) in self.attributes.items():
            try:
                minimum_v = minimum[k]
            except KeyError:
                print 'key error'
                minimum_v = None
            try:
                maximum_v = maximum[k]
            except KeyError:
                print 'key error'
                maximum_v = None
            sim[k] = v.similarity(case.attributes[k],minimum_v,maximum_v)
        similarity = sum(sim.values())

        return similarity
