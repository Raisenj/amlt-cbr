from abc import ABCMeta, abstractproperty, abstractmethod
import numpy

class Attribute(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def askValue(self):
        """ Returns the attribute name """
        return self.__value

    @abstractmethod
    def similarity(self,value):
        """ Returns the attribute name """


class RealAttr(Attribute):

    def __init__(self, value):
        self.__value = float(value)

    def askValue(self):
        """ Returns the attribute name """
        return self.__value
    def similarity(self, value):
        ## Normal distance
        return abs(self.__value-value.__value)

class CategoricalAttr(Attribute):

    def __init__(self, value):
        self.__value = str(value)

    def askValue(self):
        """ Returns the attribute name """
        return self.__value
    def similarity(self,value):
        ## Equal
        if self.__value == value:
            return  0
        else:
            return  1

        
