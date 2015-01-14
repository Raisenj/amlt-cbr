from Attributes import RealAttr, CategoricalAttr, Attribute

class Case():

    def __init__(self, attributes, label):
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
        for k in self.label.keys():
            print k, ': ',  self.label[k].askValue()
        print '=================='
        print '\n'



