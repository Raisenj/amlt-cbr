from Attributes import RealAttr, CategoricalAttr, Attribute

class Case():
    _attributes = {}
    _solution = None
    _utility = None
    _evaluation = None

    def __init__(self,attributes,solution):
        self._attributes = attributes
        self._solution = solution

    def printCase(self):
        print '\n'
        print '====== CASE ======'
        for k in self._attributes.keys():
            if isinstance(self._attributes[k], Attribute):
                print 'name: ', k,', value: ', self._attributes[k].askValue()
        print 'Solution: ', self._solution
        print '=================='
        print '\n'
        

    
