from abc import ABCMeta, abstractproperty, abstractmethod
from CBRFunctions import normalize
import numpy

class Attribute(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def askValue(self):
        """ Returns the attribute name """
        return self.__value

    @abstractmethod
    def similarity(self,value, minimum_v = None, maximum_v = None):
        """ Returns the attribute name """
    
    @abstractmethod
    def attrType(self):
        """ returns type"""


class RealAttr(Attribute):

    def __init__(self, value):
        self.__value = float(value)

    def askValue(self):
        """ Returns the attribute name """
        return self.__value
    def similarity(self, value, minimum_v, maximum_v):
        ## Normal distance
        sim = abs(normalize(self.__value,minimum_v, maximum_v)-
                normalize(value.askValue() ,minimum_v, maximum_v))
        return sim
    
    def attrType(self):
        return 'r'

class CategoricalAttr(Attribute):

    def __init__(self, value):
        self.__value = str(value)

    def askValue(self):
        """ Returns the attribute name """
        return self.__value

    def attrType(self):
        return 'c'


    def similarity(self,value, minimum_v = None, maximum_v = None):
        ## Equal
        if self.__value == value:
            return  0
        else:
            return  1

        
