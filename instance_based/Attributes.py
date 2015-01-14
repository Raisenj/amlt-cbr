from abc import ABCMeta, abstractproperty, abstractmethod

class Attribute(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def askValue(self):
        """ Returns the attribute name """
        return self._value


class RealAttr(Attribute):
    _value = None

    def __init__(self, value):
        self._value = value 

    def askValue(self):
        """ Returns the attribute name """
        return self._value

class CategoricalAttr(Attribute):
    _value = None

    def __init__(self, value):
        self._value = value 
    
    def askValue(self):
        """ Returns the attribute name """
        return self._value

