from abc import ABCMeta, abstractproperty, abstractmethod
from CBRFunctions import normalize, stringSim
import numpy

""" This class implements the kind of attributes that the CBR can
handle. If a developer wants to introduce a new kind of attribute,
this is the place"""

class Attribute(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def askValue(self):
        """ Returns the attribute name """

    @abstractmethod
    def similarity(self, value, minimum_v = None, maximum_v = None):
        """ Returns the attribute name """

    @abstractmethod
    def attrType(self):
        """ returns type"""

    def __eq__(self,real):
            if self.__value == real.__value:
                return True
            else:
                return False


class RealAttr(Attribute):

    def __init__(self, value):
        self.__value = float(value)

        
    def askValue(self):
        return self.__value

    def similarity(self, value, minimum_v, maximum_v):
        ## Normal distance
        return abs(normalize(self.__value, minimum_v, maximum_v) -
                  normalize(value.askValue(), minimum_v, maximum_v))

    def attrType(self):
        return 'r'

class CategoricalAttr(Attribute):

    def __init__(self, value):
        self.__value = str(value)

    def askValue(self):
        return self.__value

    def attrType(self):
        return 'c'

    def similarity(self, value, minimum_v = None, maximum_v = None):
        ## Equal
        return (1-float(self.__value == value.askValue))

class StringAttr(Attribute):

    def __init__(self, value):
        self.__value = str(value)

    def askValue(self):
        return self.__value

    def attrType(self):
        return 's'

    def similarity(self, value, minimum_v = None, maximum_v = None):
        #print stringSim(self.__value, value.askValue())
        return stringSim(self.__value, value.askValue())


