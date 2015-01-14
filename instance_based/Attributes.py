from abc import ABCMeta, abstractproperty, abstractmethod

class Attribute(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def askValue(self):
        """ Returns the attribute name """
        return self.__value

class RealAttr(Attribute):

    def __init__(self, value):
        self.__value = float(value)

    def askValue(self):
        """ Returns the attribute name """
        return self.__value

class CategoricalAttr(Attribute):

    def __init__(self, value):
        self.__value = str(value)

    def askValue(self):
        """ Returns the attribute name """
        return self.__value

