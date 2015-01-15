from Attributes import RealAttr, CategoricalAttr, Attribute

class Case():

    def __init__(self, attributes, label=None):
        self.attributes = attributes
        self.label = label
        self.utility = None
        self.evaluation = None

    def __del__(self):
        pass

    def printCase(self):
        print '\n'
        print '====== CASE ======'
        for k in self.attributes.keys():
            print k, ': ', self.attributes[k].askValue()
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

    def names(self):
        names = []
        for name in self.attributes.keys():
            names.append(name)
        names.append(self.label.keys()[0])
        return names

    def labelName(self):
        return self.label.keys()[0]

    def similarity(self,case):
        s = []
        for k in self.attributes.keys():
            s.append(self.attributes[k].similarity(case.attributes[k]))
        return s




